import pathlib
import click
import jinja2
import toml
import pendulum
import subprocess
import shlex


def load_template(name):
    '''
    Return the singularity recipe template as unicode text
    '''
    template = pathlib.Path(name).read_text()
    return template

@click.command()
@click.option("--shovill_version", default=None)
@click.option("--spades_version", default=None)
@click.option("--skesa_version", default=None)
@click.option("--author", default=None)
@click.option("-c", "--config", default="config.toml")
def update_singularity( shovill_version, spades_version,skesa_version,author, config):

    '''
    update the singularity recipe for new version of snippy
    '''

    config = toml.load('config.toml')

    if shovill_version is not None:
        config['shovill_version'] = shovill_version
    if spades_version is not None:
        config['spades_version'] = spades_version
    if skesa_version is not None:
        config['skesa_version'] = skesa_version
    if author is not None:
        config['author'] = author
    
    loader = jinja2.FunctionLoader(load_template)
    env = jinja2.Environment(loader=loader)
    SINGULARITY_RECIPE = env.get_template("assemblers.singularity").render(config)
    # create global version
    global_recipe = pathlib.Path("Singularity")
    global_recipe.write_text(SINGULARITY_RECIPE)



if __name__ == "__main__":
    update_singularity()
