"""Mine SCCM data for 3rd-party vulnerabilities.

Usage:

listpass.py [-h] [--help]
            [-d dirs] [--dirs=dirs]
            [--list=one/full]
            [-x dirs] [--exclude=dirs]

-h --help   Produce this help messages

-d directories --dirs=directories

            Specify the list of directories to print

-l --list   Type of listing to produce
            "full"  dump everything
            "topline"   dump first line only

-x directores --exclude=directories

            Specify list of directories / files to exclude

Function
--------

Dump the contents of the pass tree of passwords.

Prints text for each password in set of folders selected (except
    those in excluded directories / files.)

Prints either full text, or just the top line (containing the actual
    password.

Assumptions
-----------

1. Key is inserted and pass is able to dump pwds
2. Only 1 level of folders is present.
3. Main password store is .password.

Examples
--------

    python listpass.py -d "srv,kp" --list=full
"""

import argparse
import subprocess
import os
import sys

######
#   Globals
######
PASSDIR = "/.password-store"
GPGEXT = ".gpg"
LIST_ALL = "all"

# Don't export any symbols
__all__ = ()


######
#   Mainline code
######

def main():
    """Handle case where pgm is called as a script from the cmd line."""
    #####
    #   Parse the input arguments
    #####

    parser = argparse.ArgumentParser(
        description='List contents of pass tree of passwords.'
        )

    parser.add_argument(
        '--oneliner',
        action='store_true',
        help='Print oneliner (i.e. pwd only) listing'
        )

    parser.add_argument(
        '-d', '--dirs',
        default=LIST_ALL,
        nargs='+',
        help='Desired directories to list.'
        )

    parser.add_argument(
        '-x', '--exclude',
        default='.git',
        nargs='+',
        help='Desired directories / files to exclude.'
        )


    args = parser.parse_args()


    # Determine list of excluded directories

    if isinstance(args.exclude, list):
        exclude_list = [".git"] + args.exclude
    else:
        exclude_list = [args.exclude]

    print "Excluded directories: {0}".format(exclude_list)

    # Directories to process
    if isinstance(args.dirs, str):
        include_list = [args.dirs]
    else:
        include_list = args.dirs

    myout = ""

    ######
    #   Walk the pass pwd store directory
    ######

    rootdir = os.path.expanduser("~") + PASSDIR

    # print "debug1: {0}, {1}".format(rootdir, exclude_list)

    for dirname, subdir_list, filelist in os.walk(rootdir):

        # print "debug2: {0}, {1}, {2}".format(dirname, subdir_list, filelist)

        if os.path.isdir(dirname):

            # print "debug3: {0}, {1}, {2}".format(
                                                # dirname,
                                                # subdir_list,
                                                # filelist
                                                # )

            # don't bother with control files in directory root
            if dirname == rootdir:
                # print "debug 4: exclude root directory"
                continue

            # exclude directories in the exclude list
            is_excluded = False
            for d in exclude_list:
                if d in dirname:
                    # print "   Excluding {0}".format(dirname)
                    is_excluded = True
                    break
            if is_excluded:
                continue

            foldername = os.path.basename(os.path.normpath(dirname))

           # Check if listing only specific folders
            if not (LIST_ALL in include_list):
                is_excluded = True
                for d in include_list:
                    if d == foldername:
                        is_excluded = False
                if is_excluded:
                    continue

            for f in filelist:
                # Ignore extraneous files
                (filename, file_extension) = os.path.splitext(f)

                # print "debug5 {0} {1} ".format(f, os.path.splitext(f))

                if file_extension == GPGEXT:

                    passname = foldername + "/" + filename

                    print "=====Pwd: {0}=====".format(passname)

                    s1 = subprocess.check_output(['pass', passname])

                    if args.oneliner:
                        # Just want listing of 1st lines containing the
                        #    actual pwds
                        myout = myout + '{0}: {1}\n'.format(
                                                    passname,
                                                    s1.split('\n', 1)[0]
                                                    )
                    else:
                        print s1


    if args.oneliner:
        print myout


if __name__ == '__main__':
    sys.exit(main())

