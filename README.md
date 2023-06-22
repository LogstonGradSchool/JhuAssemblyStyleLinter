# Assembly Style Linter

- For: Computer Organization - 605.204
- Instructor: Charles Kann

## Analysis


## Install

```
pip install jhu-assembly-linter
```

## Usage

Pip install from the [releases page](https://github.com/LogstonGradSchool/JhuAssemblyStyleLinter/releases). Then ...

```
jhu-assembly-linter ./path/to/file.s
```

For a whole directory:

```
find . -name "*.s" | xargs -I{} jhu-assembly-linter  {}
```
