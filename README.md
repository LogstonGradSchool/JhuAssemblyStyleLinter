# Assembly Style Linter

- For: Computer Organization - 605.204
- Instructor: Charles Kann

## Analysis


## Install

```
pip install jhu-assembly-linter
```

## Usage

Pip install from the [releases
page](https://github.com/LogstonGradSchool/JhuAssemblyStyleLinter/releases).
Then ...

```
$ jhu-assembly-linter ./path/to/file.s

E:: Tab found. Only spaces allowed.
18:     LDR x0, =helloWorld
    ^
E:: Instruction is not uppercase.
19:     mov     w8, #64     /* write is syscall #64 */
        ^
E:: Non-functional whitespace found.
20: 
    ^^^^^
E:: File name does not end with "Main" when it should.
21: main:
```

For a whole directory:

```
find . -name "*.s" | xargs -I{} jhu-assembly-linter  {}
```

### Tests

```
tox
```

### Deployment

```
poetry build
poetry publish
```
