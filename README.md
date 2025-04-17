# Herbie Plugin Tutorial

This is a demonstration of writing a Herbie plugin to add a custom model template.

I would love it if you contributed a model template to the main Herbie repository, but there may be cases when you need a custom model template.

- You have local GRIB2 files you want to access using Herbie.
- You need to handle an existing model a little differently.
- You have access to model data on a private network.
- You want to test a new or updated model template before contributing to Herbie.
- Any other reasons? Let me now.

Plugins let you add a custom model template that Herbie can discover on import.

For example, if you install

```bash
pip install herbie-data
pip install herbie-plugin-tutorial
```

Then Herbie can use any of the custom model templates defined in herbie-plugin-tutorial.

Making a model template is a craft, and has some historical and peculiar behaviors that because Herbie was written by me over seven years ago. It is what it is.

## Begin

I created this `herbie-data-tutorial` repository using [uv](https://docs.astral.sh/uv/). I spcified Python 3.10 when creating the library since that is the minimum version required for Herbie.

```bash
uv init --lib herbie-plugin-tutorial --python 3.10
```

Then I created a repo of the same name on GitHub and updated the remote.



