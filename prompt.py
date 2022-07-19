import click


@click.command()
@click.option('--name', prompt=True)
def prompt(name):
    click.echo(f"Hello {name}")


if __name__ == '__main__':
    prompt()
