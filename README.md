# Herbie Plugin Tutorial

This is a demonstration of writing a plugin for [Herbie](https://github.com/blaylockbk/Herbie) to add a custom model template.

I would love it if you contributed a model template to the main Herbie repository, but there may be cases when you need a custom model template.

- You have local GRIB2 files you want to access using Herbie (e.g. a WRF or MPAS simulation with GRIB2 output).
- You need to handle an existing model a little differently.
- You have access to GRIB2 model data on a private network.
- You want to test a new or updated model template before contributing to Herbie.
- Do you have any other uses? Let me now!

## How it works

Plugins let you add a custom model template that Herbie can discover on import.

For example, if you install herbie and this repo

```bash
pip install herbie-data

git clone https://github.com/blaylockbk/herbie-plugin-tutorial.git
cd herbie-plugin-tutorial
pip install -e .
```

Then Herbie can use any of the custom model templates defined in `herbie-plugin-tutorial`.

## Begin

I created this `herbie-data-tutorial` repository using [uv](https://docs.astral.sh/uv/). I spcified Python 3.10 when creating the library since that is the minimum version required for Herbie.

```bash
uv init --lib herbie-plugin-tutorial --python 3.10
```

Then I added herbie-data as a dependency (the plugin would be useless if it didn't have herbie-data installed).

```bash
uv add herbie-data
```

Finally, I created the repo on GitHub and gave it an MIT license so I can share it with you.

## Update pyproject.toml

Next, add entry points to `pyproject.toml` so Herbie knows this package is a plugin. The key and value in the second line should match your plugin name.

```toml
[project.entry-points."herbie.plugins"]
herbie_plugin_demo = "herbie_plugin_demo"
```

## Create your custom model template

Next, create your custom model templates. These are placed in the package's `__init__.py` file. Making a model template is a craft, and has some historical and peculiar behaviors; both because Herbie was written by me when I had much less Python experience and because its hard supporting lots of edge cases. Model tempalte files are what they are.

Look at the `herbie-plugin-tutorial/src/herbie_plugin_tutorial/__init__.py` file in this repo and study the two example classes:

1. `hrrr_analysis` - Custom behavior for accessing HRRR model (only discover files on AWS and only analysis fields)
2. `bmw` - Local GRIB2 files output from a fictional model _BMW_ "Brian's Model of Weather"

Here are some things to remember when writing a model template:

1. The class is the name a Herbie uses calls the model (i.e., `model='bmw'`). **The class name _must_ be lower case!** Herbie changes the user input to lower case, so if they call `model='HRRR'` it will actually get `model='hrrr'`.

1. `self.DESCRIPTION` and `self.DETAILS` are just convenient metadata.

1. `self.PRODUCTS` must have at least one entry. If a Herbie user doesn't specify a `product=None`, then the first is used by default. This value is available to build the file path as `self.product`.

1. `self.SOURCES` can have one or more key-value pairs. Herbie will loop through each SOURCE until it finds a file that exists. Preface the key with `local` if you want Herbie to search the local path instead of a web URL.

1. Look at [existing model templates](https://github.com/blaylockbk/Herbie/tree/main/herbie/models) for more complex examples.

## Install your plugin

From the root of your new plugin (the directory the `pyproject.toml` file exists) install your package with pip

```bash
pip install -e .
```

## Use your custom model in Herbie

Once installed, you can then access your custom model templates in Herbie.

```python
from herbie import Herbie
```

Prints the following to confirm you have custom templates available:

```
Herbie: model template 'hrrr_analysis' from custom plugin was added to globals.
Herbie: model template 'bmw' from custom plugin was added to globals.
```

Now Herbie can use your custom template

```python
H = Herbie("2025-01-01", model="hrrr_analysis")
```

```python
H = Herbie("2025-01-01", model="bmw", domain='3a')

# Note: This example will never find anything because it is a fictitious model.
```
