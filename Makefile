.PHONY: build install test clean lint format

RELEASE_TYPE = Release
PY_SRC = src/pysrc
CPP_SRC = src/cppsrc

build: install_cpp install_py
	cd build && cmake .. -DCMAKE_TOOLCHAIN_FILE=$(RELEASE_TYPE)/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=$(RELEASE_TYPE) -G Ninja
	cd build && cmake --build .
	@cp -f build/*.so $(PY_SRC)

install_cpp:
	conan install . --build=missing

install_py:
	poetry install

test_cpp: build
	@cd build && ./intern_tests

test_py: build
	@poetry run pytest $(PY_SRC)/test/unit

test_int: build
	@poetry run pytest $(PY_SRC)/test/int/

test: test_int test_py test_cpp lint_cpp lint_py

clean:
	@rm -rf build
	@rm -f $(PY_SRC)/*.so
	rm out.txt

lint_cpp: build
	find $(CPP_SRC) -name "*.cpp" -or -name "*.hpp" | xargs clang-tidy -p=build
	find $(CPP_SRC) -name "*.cpp" -or -name '*.hpp' | xargs clang-format --dry-run --Werror

lint_py: build
	poetry run mypy $(PY_SRC)
	poetry run ruff check $(PY_SRC)
	poetry run ruff format --check $(PY_SRC)

format:
	find $(CPP_SRC) -name '*.cpp' -o -name '*.hpp' | xargs clang-format -i
	poetry run ruff format $(PY_SRC)
	poetry run ruff check --fix $(PY_SRC)
	clang-format -i src/cppsrc/*.hpp
	clang-format -i src/cppsrc/*.cpp
	clang-format -i src/cppsrc/test/*.cpp