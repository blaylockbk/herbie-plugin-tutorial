# Herbie Plugin Tutorial

This is a demonstration of writing a plugin for [Herbie](https://github.com/blaylockbk/Herbie) to add custom model templates.

I’d love for you to contribute your model template to the main Herbie repository—but sometimes you might need your own:

- You have local GRIB2 files you want to access using Herbie (e.g., a WRF or MPAS simulation).
- You need to handle an existing model a little differently.
- You have access to GRIB2 model data on a private network.
- You want to test a new or updated model template before contributing upstream.
- Other reasons? Let me know!

## How it works

Herbie plugins let you add custom model templates that Herbie can discover when imported.

For example, after installing Herbie and this plugin tutorial:

```bash
pip install herbie-data

git clone https://github.com/blaylockbk/herbie-plugin-tutorial.git
cd herbie-plugin-tutorial
pip install -e .
```

Herbie can now use the custom templates defined in this .`herbie-plugin-tutorial` plugin.

## Creating a plugin

I created this `herbie-data-tutorial` repository using [uv](https://docs.astral.sh/uv/) and specified Python 3.10 (the minimum required by Herbie):

```bash
uv init --lib herbie-plugin-tutorial --python 3.10
```

Then I added `herbie-data` as a dependency (because the plugin without Herbie would not be very useful).

```bash
uv add herbie-data
```

To register this package as a Herbie plugin, add the following endpoints to your `pyproject.toml`. The key (e.g., `herbie_plugin_demo`) should match your plugin's name.

```toml
[project.entry-points."herbie.plugins"]
herbie_plugin_demo = "herbie_plugin_demo"
```

### Making a custom model template

Your model templates live in your plugin’s __init__.py file.

Model templates are a bit of a craft due to some historical quirks, a few odd conventions (Herbie's grown over time!), and support for a lot of edge cases. Still, the basic structure is simple.

Take a look at `herbie-plugin-tutorial/src/herbie_plugin_tutorial/__init__.py`, which includes two example templates:

1. `hrrr_analysis` — A custom version of the HRRR model that only finds analysis fields from AWS.
2. `bmw` — Local GRIB2 files output from a fictional dataset: _BMW_ "Brian's Model of Weather"


### Tips for writing a template

1. The class name must be lowercase! Herbie lowercases the `model=` input, so `model='HRRR'` becomes `model='hrrr'`.

1. Set `self.DESCRIPTION` and `self.DETAILS` for helpful metadata.

1. `self.PRODUCTS` must have at least one entry. If the user doesn't provide a `product=`, Herbie uses the first one by default. This value is stored as `self.product`.

1. `self.SOURCES` is a dictionary of key-value pairs. Herbie will try each one in order until it finds a valid file. Prefix a key with `local` if the file is on disk instead of on a remote server.

Look at [existing model templates](https://github.com/blaylockbk/Herbie/tree/main/herbie/models) for more examples.

## Install your plugin

From the root of your new plugin (where `pyproject.toml` lives) install your package with:

```bash
pip install -e .
```

## Use your custom model in Herbie

Once installed, Herbie will automatically detect and register your custom templates:

```python
from herbie import Herbie
```

You’ll see something like this in your console:

```
Herbie: model template 'hrrr_analysis' from custom plugin was added to globals.
Herbie: model template 'bmw' from custom plugin was added to globals.
```

You can now use your custom model like any built-in Herbie model:

```python
H = Herbie("2025-01-01", model="hrrr_analysis")
```

```python
H = Herbie("2025-01-01", model="bmw", domain='3a')

# Note: This example will never find anything because BMW is a fictional model for demonstration.
```
