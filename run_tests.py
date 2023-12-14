"""Test Pure Python functionality"""

import os
import sys
import nose
import flaky.flaky_nose_plugin as flaky

# For nose
if sys.version_info[0] == 3:
    import collections
    collections.Callable = collections.abc.Callable


if __name__ == "__main__":
    print("Initialising Maya..")
    from maya import standalone, cmds
    standalone.initialize()
    cmds.loadPlugin("matrixNodes", quiet=True)

    argv = sys.argv[:]
    argv.extend([
        "--verbose",
        "--with-doctest",

        "--with-flaky",
        "--with-coverage",
        "--cover-html",
        "--cover-package", "cmdx",
        "--cover-erase",
        "--cover-tests",

        "tests.py",
        "test_performance.py",
        "cmdx.py",
    ])

    cmds.colorManagementPrefs(cmEnabled=False, edit=True)

    result = nose.main(
        argv=argv,
        addplugins=[flaky.FlakyPlugin()],

        # We'll exit in our own way,
        # since Maya typically enjoys throwing
        # segfaults during cleanup of normal exits
        exit=False
    )

    if os.getenv("TRAVIS_JOB_ID"):
        import coveralls
        coveralls.wear()
    else:
        sys.stdout.write("Skipping coveralls\n")

    if os.name == "nt":
        # Graceful exit, only Windows seems to like this consistently
        standalone.uninitialize()

    # Trust but verify
    os._exit(0 if result.success else 1)
