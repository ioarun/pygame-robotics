# buid : python setup.py build
# installer : python setup.py bdist_msi

import cx_Freeze

executables = [cx_Freeze.Executable("slither.py")]

cx_Freeze.setup(
	name="Slither",
	options={"build_exe":{"packages":["pygame"], "include_files":["apple.png", "snake.png"]}},
	description = "Slither Game",
	executables = executables
	)