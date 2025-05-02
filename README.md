<div align=center>
<img src="https://raw.githubusercontent.com/blaylockbk/herbie-plugin-tutorial/refs/heads/main/images/herbie-tires.png" width=250>

# Herbie Plugin Tutorial

</div>

This tutorial shows how to write a plugin for [Herbie](https://github.com/blaylockbk/Herbie) to add custom model templates—like giving Herbie a new set of tires.

You might need your own model template when:

- You have local GRIB2 files (e.g., WRF/MPAS output) you'd like to access with Herbie.
- You have access to GRIB2 data on a private network.
- You want to override behavior of an existing model temple.
- You want to iterate on a new model template before contributing upstream.

## What is a Herbie model template?

A _model template_ in Herbie is a Python class that defines where Herbie looks for weather model datasets. Herbie comes with a bunch of [model templates](https://github.com/blaylockbk/Herbie/tree/main/src/herbie/models) you can look at for reference. When you import Herbie, it loads its model templates, and then Herbie looks for any templates from installed plugins.

## Project structure

Here's what your plugin project should look like:

```
herbie-plugin-tutorial/
├── pyproject.toml
└── src/
    └── herbie_plugin_tutorial/
        └── __init__.py  # contains your model templates
```

## Create the plugin project

I used [uv](https://docs.astral.sh/uv/) to create this example plugin:

```bash
uv init --lib herbie-plugin-tutorial --python 3.10
cd herbie-plugin-tutorial
uv add herbie-data
```

- I set `--python 3.10` because that is Herbie's minimum version
- Add `herbie-data` as a dependency, because what good is a plugin without the main package.

To register your plugin with Herbie, add the following to your `pyproject.toml`:

```toml
[project.entry-points."herbie.plugins"]
hrrr_analysis = "herbie_plugin_tutorial:hrrr_analysis"
bmw = "herbie_plugin_tutorial:bmw"
```

### Making a custom model template

Your model templates live in your plugin’s `__init__.py` file.

Model templates are a bit of a craft due to some historical quirks, a few odd conventions (Herbie's grown over time!), and support for a lot of edge cases. Still, the basic structure is simple.

Take a look at this plugin's [`__init__.py`](https://github.com/blaylockbk/herbie-plugin-tutorial/blob/main/src/herbie_plugin_tutorial/__init__.py), which includes two example templates:

1. `hrrr_analysis` — A custom template for the HRRR model that only locates analysis fields from AWS.
2. `bmw` — Local GRIB2 files output from a fictional dataset _BMW_ "Brian's Model of Weather"

> [!TIP]
> 
> 1. Class names must be lowercase! Herbie lowercases the `model=` input, so `model='HRRR'` becomes `model='hrrr'`.
> 
> 1. Set `self.DESCRIPTION` and `self.DETAILS` for helpful metadata.
> 
> 1. `self.PRODUCTS` must have at least one entry. If the user doesn't provide a `product=`, Herbie uses the first one by default.
> 
> 1. `self.SOURCES` is a dictionary of key-value pairs. Herbie will try each one in order until it finds a valid file. Prefix a key with `local` if the file is on disk instead of on a remote server.
> 
> 1. `self.LOCALFILE` is how you specify what the file name will be when it is downloaded. Setting to `f"{self.get_remoteFileName}"` simply says to keep the original name of the file.
>
> Look at [existing model templates](https://github.com/blaylockbk/Herbie/tree/main/herbie/models) for more examples.


## Use your Herbie plugin

Install the plugin `pip install -e .` in your environment to use your custom templates.


Let's walk through using this plugin in a new project using uv.

```bash
uv init new_project
cd new_project
uv add herbie-data --extra extras
uv add --editable ../herbie-plugin-tutorial
```

- I used `--editable` so I could debug the plugin if needed.

Then launch Python

```bash
uv run python
```

Importing Herbie automatically registers your templates.

```python
from herbie import Herbie
```

You should see output like this when a plugin loads:

> ```
> Herbie: Added model 'bmw' from herbie-plugin-tutorial.
> Herbie: Added model 'hrrr_analysis' from herbie-plugin-tutorial.
> ```

Now you can use those models in Herbie.

```python
H = Herbie("2023-01-01", model="hrrr_analysis")

# This one doesn't find anything because its a fictitious model
H = Herbie("2022-01-01", model="bmw", domain='hello')
```

You can look at the possible source locations with `H.SOURCES`

```python
>>> from herbie import Herbie
>>> H = Herbie("2022-01-01", model="bmw", domain='hello')
💔 Did not find ┊ model=bmw ┊ product=default ┊ 2022-Jan-01 00:00 UTC F00
>>> H.SOURCES
{'local_main': '/path/to/bmw/model/output/bmw/gribfiles/2022010100/my_file.t00z.f00_hello.grib2'}
```

## Fin

Please [tell me](https://github.com/blaylockbk/Herbie/discussions/categories/show-and-tell) if you made a useful plugin. Consider publishing it on GitHub or PyPI if you think others would like it too.
