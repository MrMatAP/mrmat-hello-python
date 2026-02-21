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
import os
import typing

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
)

from .hashi_vault_settings import HashiVaultAuthMethod, HashiVaultSettingsSource


class VaultSettingsBase(BaseSettings):
    """
    A base class for settings, of which some come out of a vault
    """

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: typing.Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            HashiVaultSettingsSource(settings_cls,
                                     vault_url=os.getenv('VAULT_URL'),
                                     vault_auth_method=HashiVaultAuthMethod(os.getenv('VAULT_AUTH_METHOD')),
                                     vault_username=os.getenv('VAULT_USERNAME'),
                                     vault_password=os.getenv('VAULT_PASSWORD'),
                                     vault_namespace=os.getenv('VAULT_NAMESPACE')))


