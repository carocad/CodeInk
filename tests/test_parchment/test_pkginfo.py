import os

from codeink.parchment import pkginfo

def test_get_directories():
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    pig_path = os.path.join(parent_dir, 'guinea-pig')
    correct_value = set([pig_path,
                        os.path.join(pig_path, 'cage1'),
                        os.path.join(pig_path, 'cage2')])
    # check getting all possible directories with .py extension files
    assert correct_value == set(pkginfo.get_directories(pig_path, '.py'))
    # check that an empty iterable is returned for an empty directory
    cage3_dir = os.path.join(pig_path, 'cage3')
    assert set() == set(pkginfo.get_directories(cage3_dir))

def test_is_package():
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    pig_path = os.path.join(parent_dir, 'guinea-pig')
    # test correct package recognizition
    assert True == pkginfo.is_package(pig_path)
    # test correct non-package recognizition
    pig3_dir = os.path.join(pig_path, 'cage3')
    assert False == pkginfo.is_package(pig3_dir)

def test_get_modules():
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    pig_path = os.path.join(parent_dir, 'guinea-pig')
    dirs = pkginfo.get_directories(pig_path)
    # test correct module recognizition
    correct_value = set([os.path.join(pig_path, 'cage1', 'pig1.py'),
                         os.path.join(pig_path, 'cage2', 'pig2.py'),
                         os.path.join(pig_path, 'lab_assistant.py')])
    assert correct_value == set(pkginfo.get_modules(dirs))
    # test correct non-module recognizition
    cage3_dir = [os.path.join(pig_path, 'cage3')]
    assert set() == set(pkginfo.get_modules(cage3_dir))

def test_filter_modules():
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    pig_path = os.path.join(parent_dir, 'guinea-pig')
    dirs = pkginfo.get_directories(pig_path)
    # test not matching module paths
    modules = list(pkginfo.get_modules(dirs))
    patterns = ['*foo*'] # nothing to filter
    filtered_modules = pkginfo.filter_modules(modules, patterns)
    assert modules == filtered_modules
    # test matching module paths
    assert [] == pkginfo.filter_modules(modules, ['*test*'])

def test_find_root_pkg():
    cwd = os.path.dirname(__file__)
    parent_dir = os.path.dirname(cwd)
    pig_path = os.path.join(parent_dir, 'guinea-pig')
    pig1_path = os.path.join(pig_path, 'cage1', 'pig1.py')
    assert parent_dir == pkginfo.find_root_pkg(pig1_path)
