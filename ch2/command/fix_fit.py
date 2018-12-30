
from sys import stdout

from .args import PATH, DROP, OUTPUT, SLICES, RAW, WARN, MIN_SYNC_CNT, MAX_RECORD_LEN, MAX_DROP_CNT, MAX_BACK_CNT, \
    MAX_FWD_LEN, DISCARD, FORCE, VALIDATE, no, ADD_HEADER, HEADER_SIZE, PROTOCOL_VERSION, PROFILE_VERSION, mm
from ..fit.fix import fix
from ..fit.profile.profile import read_fit


def fix_fit(args, log, db):
    '''
## fix-fit

    > ch2 fix-fit PATH -o PATH --drop

Try to fix a corrupted fit file.

By default, the length and checksum are updated.

If `--slices` is specified then the given slices are taken from the data and used to construct a new file.

If `--drop` is specified then the program tries to find appropriate slices by discarding data until all the
remaining data can be parsed.

The length and checksums are updated as appropriate.

### Examples

    > ch2 fix-fit FILE.FIT --slices 1000:

Will attempt to drop the first 1000 bytes from the given file.

    > ch2 fix-fit data/tests/personal/8CS90646.FIT --drop --discard

Will attempt to fix the given file (in the test data from git).
    '''

    data = read_fit(log, args[PATH])
    log.info('Read %d bytes' % len(data))

    if not args[FORCE]:
        log.warning('Records are not evaluated (%s)' % no(FORCE))

    data = fix(log, data, add_header=args[ADD_HEADER], drop=args[DROP], slices=args[SLICES],
               warn=args[WARN], force=args[FORCE], validate=args[VALIDATE],
               header_size=args[HEADER_SIZE], protocol_version=args[PROTOCOL_VERSION], profile_version=args[PROFILE_VERSION],
               min_sync_cnt=args[MIN_SYNC_CNT], max_record_len=args[MAX_RECORD_LEN],
               max_drop_cnt=args[MAX_DROP_CNT], max_back_cnt=args[MAX_BACK_CNT], max_fwd_len=args[MAX_FWD_LEN])

    out_path = args[OUTPUT]
    if out_path:
        with open(out_path, 'wb') as out:
            out.write(data)
        log.info('Wrote data to %s' % out_path)
    elif args[DISCARD]:
        log.info('Discarded output')
    elif args[RAW]:
        log.info('Writing binary data to stdout')
        stdout.buffer.write(data)
    else:
        log.info('Writing hex data to stdout')
        stdout.write(data.hex())

