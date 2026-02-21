#  MIT License
#
#  Copyright (c) 2026 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import enum
import typing

import hvac
import hvac.exceptions
import pydantic
import pydantic.fields
import pydantic_settings

from .exceptions import VaultSettingsException


@enum.unique
class HashiVaultAuthMethod(enum.Enum):
    """
    An enumeration of Hashicorp Vault authentication methods
    """
    USERPASS = 'userpass'


class HashiVaultSettingsSource(pydantic_settings.PydanticBaseSettingsSource):
    """
    A settings source that provisions settings from a Hashicorp Vault instance.
    """

    def __init__(self, settings_cls: typing.Type[pydantic_settings.BaseSettings],
                 vault_url: str,
                 vault_auth_method: HashiVaultAuthMethod,
                 vault_username: str,
                 vault_password: str,
                 vault_namespace: str | None = None):
        """

        Args:
            settings_cls (typing.Type[BaseSettings]): Type of the model being enriched by this settings source
            vault_url (str): The Hashicorp Vault URL from where to obtain the secrets from
            vault_auth_method ():
            vault_username ():
            vault_password ():
            vault_namespace (str): The namespace, if applicable, within Vault where the secrets are stored. None by default.

        Raises:
            VaultSettingsException: If the vault authentication method is not supported or authentication fails
        """
        super().__init__(settings_cls)
        self._vault: hvac.Client = hvac.Client(url=vault_url,
                                               namespace=vault_namespace,
                                               verify=True)
        self._vault.secrets.kv.default_kv_version = 2
        match vault_auth_method:
            case HashiVaultAuthMethod.USERPASS:
                self._vault.auth.userpass.login(username=vault_username,
                                                password=vault_password)
            case _:
                raise VaultSettingsException(code=400, msg=f'Unsupported vault method: {vault_auth_method}')
        if not self._vault.is_authenticated():
            raise VaultSettingsException(code=400, msg='Unable to authenticate with Vault')


    def get_field_value(self, field: pydantic.fields.FieldInfo, field_name: str) -> tuple[typing.Any, str, bool]:
        """
        Obtain the field value from Hashicorp Vault.
        Args:
            field (pydantic.fields.FieldInfo): The field information as declared in the model
            field_name (str): The field name

        Returns:
            The raw field data from HashiCorp Vault in JSON format

        Raises:
            VaultSettingsException: If the secret is not found in Vault
        """
        try:
            secret = self._vault.secrets.kv.read_secret(path=field.json_schema_extra['vault_secret'])
            return secret['data']['data'], field_name, True
        except hvac.exceptions.InvalidPath:
            raise VaultSettingsException(code=404, msg=f'Secret not found: {field.json_schema_extra["vault_secret"]}')

    def prepare_field_value(self,
                            field_name: str,
                            field: pydantic.fields.FieldInfo,
                            value: typing.Any,
                            value_is_complex: bool) -> typing.Any:
        """
        Transforms the raw field JSON data into the expected type as declared by the Field.
        Args:
            field_name (str): The name of the field
            field (pydantic.fields.FieldInfo): The field information as declared in the model
            value (typing.Any): The raw field data from HashiCorp Vault in JSON format
            value_is_complex (bool): Whether the field is of a complex type

        Returns:
            The field in the desired type

        Raises:
            VaultSettingsException: If the secret was found, but it does not contain the expected key
        """
        key = field.json_schema_extra.get('vault_key')
        if key not in value:
            raise VaultSettingsException(code=404, msg=f'Key {key} not found in secret')
        return value.get(key)

    def __call__(self) -> dict[str, typing.Any]:
        """
        Calls the object and constructs a dictionary representation of the field values.

        The method iterates over the fields defined in the settings class, retrieves their
        values using helper methods, processes them, and includes the non-None fields in the
        result dictionary.

        Returns:
            dict[str, typing.Any]: A dictionary containing the field names and their
            corresponding processed values.
        """
        d: typing.Dict[str, typing.Any] = {}
        for field_name, field in self.settings_cls.model_fields.items():
            value, key, value_is_complex = self.get_field_value(field, field_name)
            value = self.prepare_field_value(field_name, field, value, value_is_complex)
            if value is not None:
                d[field_name] = value
        return d


def HashiVaultField(
    default: typing.Any = ...,
    *,
    vault_secret: typing.Optional[str] = None,
    vault_key: typing.Optional[str] = None,
    **kwargs: typing.Any,
) -> typing.Any:
    """
    A custom field to extract the secret path and key from a secret in HashiCorp Vault.
    This is just eye-candy, allowing the use to specify the secret path and key directly in the model
    and avoiding type checkers to complain about the otherwise unknown kwargs. The secret can
    equally well be defined on a regular Pydantic Field, with the values going into the json_schema_extra
    attribute.
    """
    if vault_secret or vault_key:
        kwargs['json_schema_extra'] = kwargs.get('json_schema_extra', {})
        if vault_secret:
            kwargs['json_schema_extra']['vault_secret'] = vault_secret
        if vault_key:
            kwargs['json_schema_extra']['vault_key'] = vault_key
    from pydantic import Field as PydanticField
    return PydanticField(default, **kwargs)
