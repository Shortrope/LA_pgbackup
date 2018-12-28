from argparse import Action, ArgumentParser

known_drivers = ('local', 's3')

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Available drivers are 'local' & 's3'")
        namespace.driver = driver.lower()
        namespace.destination = destination


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help='URL of the PostgreSQL database to backup')
    parser.add_argument('-d', '--driver',
            help='how & where to store the backup',
            nargs=2,
            metavar=('driver', 'destination'),
            action=DriverAction,
            required=True)

    return parser

def main():
    import boto3
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()

    dumpfile =  pgdump.dump(args.url)

    if args.driver == 's3':
        client = boto3.client('s3')
        storage.s3(client, dumpfile.stdout, args.destination, 'example.sql')
    else:
        outfile = open(args.destination, 'wb')
        storage.local(dumpfile.stdout, outfile)
        outfile.close()
