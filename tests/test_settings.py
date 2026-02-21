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

import pytest

import mhpython.settings

@pytest.mark.skip(reason="Requires a vault instance to be running")
def test_vault_settings():
    """
    Test whether we can retrieve secrets from HashiCorp Vault using the HashiVaultField.
    """

    class TestVaultSettings(mhpython.settings.VaultSettingsBase):
        foo: str = mhpython.settings.HashiVaultField(description='The foo secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='foo')
        bar: str = mhpython.settings.HashiVaultField(description='The bar secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='bar')
        baz: str = mhpython.settings.HashiVaultField(description='The baz secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='baz')

    settings = TestVaultSettings()
    assert settings.foo == 'one', 'The foo secret has the expected value'
    assert settings.bar == 'two', 'The bar secret has the expected value'
    assert settings.baz == 'three', 'The baz secret has the expected value'


@pytest.mark.skip(reason="Requires a vault instance to be running")
def test_vault_settings_unknown_secret():

    class TestVaultSettings(mhpython.settings.VaultSettingsBase):
        foo: str = mhpython.settings.HashiVaultField(description='The foo secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='foo')
        bar: str = mhpython.settings.HashiVaultField(description='The bar secret',
                                                     vault_secret='mrmat-hello-python/i-dont-exist',
                                                     vault_key='bar')

    with pytest.raises(mhpython.settings.VaultSettingsException) as e:
        settings = TestVaultSettings()
    assert e.value.code == 404, 'The expected VaultSettingsException is raised'
    assert e.value.msg == 'Secret not found: mrmat-hello-python/i-dont-exist'


@pytest.mark.skip(reason="Requires a vault instance to be running")
def test_vault_settings_unknown_key():

    class TestVaultSettings(mhpython.settings.VaultSettingsBase):
        foo: str = mhpython.settings.HashiVaultField(description='The foo secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='foo')
        bar: str = mhpython.settings.HashiVaultField(description='The bar secret',
                                                     vault_secret='mrmat-hello-python/test',
                                                     vault_key='i-dont-exist')

    with pytest.raises(mhpython.settings.VaultSettingsException) as e:
        settings = TestVaultSettings()
    assert e.value.code == 404, 'The expected VaultSettingsException is raised'
    assert e.value.msg == 'Key i-dont-exist not found in secret'
