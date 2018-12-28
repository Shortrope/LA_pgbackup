import pytest
from pgbackup import pgdump      # pgbackup is our module we ar writing
import subprocess


url = 'postgres://bob@example.com:5432/db_one'

def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with the database URL
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout=subprocess.PIPE)

def test_dump_handles_os_error(mocker):
    """
    pgdump.dump returns a reasonalbe error if pg_dump insn't installed
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no shuch file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

