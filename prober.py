#!/usr/bin/env python

from __future__ import division

import sys
import logging
import os.path

from optparse import OptionParser
from operator import itemgetter

# Ensure we can see the pytls/tls subdir for the pytls submodule
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "pytls"))
from tls import *

from probes import *
import probe_db

__version__ = "0.0.4"
__author__ = "Richard J. Moore"
__email__ = "rich@kde.org"


# List all the probes we have
probes = [
    NormalHandshake(),
    NormalHandshakePFS(),
    NormalHandshake11(),
    NormalHandshake11PFS(),
    NormalHandshake12(),
    NormalHandshake12PFS(),
    NormalHandshake12PFSw13(),
    ChangeCipherSpec(),
    ChangeCipherSpec12(),
    ChangeCipherSpec12PFS(),
    OnlyECCipherSuites(),
    HighTLSVersion(),
    HighTLSVersion12(),
    HighTLSVersion12PFS(),
    VeryHighTLSVersion(),
    VeryHighTLSVersion12(),
    VeryHighTLSVersion12PFS(),
    ZeroTLSVersion(),
    ZeroTLSVersion12(),
    ZeroTLSVersion12PFS(),
    HighHelloVersion(),
    HighHelloVersionNew(),
    HighHelloVersionPFS(),
    VeryHighHelloVersion(),
    VeryHighHelloVersionNew(),
    VeryHighHelloVersionPFS(),
    ZeroHelloVersion(),
    BadContentType(),
    RecordLengthOverflow(),
    RecordLengthUnderflow(),
    Heartbeat(),
    Heartbeat12(),
    Heartbeat12PFS(),
    Heartbleed(),
    Heartbleed12(),
    Heartbleed12PFS(),
    BadHandshakeMessage(),
    InvalidSessionID(),
    InvalidSessionID12(),
    InvalidSessionID12PFS(),
    InvalidCiphersLength(),
    InvalidCiphersLength12(),
    InvalidCiphersLength12PFS(),
    InvalidExtLength(),
    InvalidExtLength12(),
    InvalidExtLength12PFS(),
    EmptyCompression(),
    EmptyCompression12(),
    EmptyCompression12PFS(),
    CompressOnly(),
    CompressOnly12(),
    CompressOnly12PFS(),
    ExtensionsUnderflow(),
    ExtensionsUnderflow12(),
    ExtensionsUnderflow12PFS(),
    DoubleClientHello(),
    DoubleClientHello12(),
    DoubleClientHello12PFS(),
    EmptyRecord(),
    EmptyRecord12(),
    EmptyRecord12PFS(),
    TwoInvalidPackets(),
    SplitHelloRecords(),
    SplitHelloRecords12(),
    SplitHelloRecords12PFS(),
    SplitHelloPackets(),
    SplitHelloPackets12(),
    SplitHelloPackets12PFS(),
    NoCiphers(),
    NoCiphers12(),
    EmptyChangeCipherSpec(),
    EmptyChangeCipherSpec12(),
    EmptyChangeCipherSpec12PFS(),
    HelloRequest(),
    HelloRequest12(),
    HelloRequest12PFS(),
    SNIWrongName(),
    SNIWrongName12(),
    SNIWrongName12PFS(),
    SNILongName(),
    SNILongName12(),
    SNILongName12PFS(),
    SNIEmptyName(),
    SNIEmptyName12(),
    SNIEmptyName12PFS(),
    SNIOneWrong(),
    SNIOneWrong12(),
    SNIOneWrong12PFS(),
    SNIWithDifferentType(),
    SNIWithDifferentType12(),
    SNIWithDifferentType12PFS(),
    SNIDifferentTypeRev(),
    SNIDifferentTypeRev12(),
    SNIDifferentTypeRev12PFS(),
    SNIOverflow(),
    SNIOverflow12(),
    SNIOverflow12PFS(),
    SNIUnderflow(),
    SNIUnderflow12(),
    SNIUnderflow12PFS(),
    SecureRenegoOverflow(),
    SecureRenegoOverflow12(),
    SecureRenegoOverflow12PFS(),
    SecureRenegoUnderflow(),
    SecureRenegoUnderflow12(),
    SecureRenegoUnderflow12PFS(),
    SecureRenegoNonEmpty(),
    SecureRenegoNonEmpty12(),
    SecureRenegoNonEmpty12PFS(),
    SecureRenegoNull(),
    SecureRenegoNull12(),
    SecureRenegoNull12PFS(),
    MaxFragmentNull(),
    MaxFragmentNull12(),
    MaxFragmentNull12PFS(),
    MaxFragmentInvalid(),
    MaxFragmentInvalid12(),
    MaxFragmentInvalid12PFS(),
    ClientCertURLsNotNull(),
    ClientCertURLsNotNull12(),
    ClientCertURLsNotNull12PFS(),
    TrustedCANull(),
    TrustedCANull12(),
    TrustedCANull12PFS(),
    TrustedCAOverflow(),
    TrustedCAOverflow12(),
    TrustedCAOverflow12PFS(),
    TrustedCAUnderflow(),
    TrustedCAUnderflow12(),
    TrustedCAUnderflow12PFS(),
    TruncatedHMACNotNull(),
    TruncatedHMACNotNull12(),
    TruncatedHMACNotNull12PFS(),
    OCSPNull(),
    OCSPNull12(),
    OCSPNull12PFS(),
    OCSPOverflow(),
    OCSPOverflow12(),
    OCSPOverflow12PFS(),
    OCSPUnderflow(),
    OCSPUnderflow12(),
    OCSPUnderflow12PFS(),
    DoubleExtension(),
    DoubleExtension12(),
    DoubleExtension12PFS(),
    UserMappingNull(),
    UserMappingNull12(),
    UserMappingNull12PFS(),
    UserMappingOverflow(),
    UserMappingOverflow12(),
    UserMappingOverflow12PFS(),
    ClientAuthzNull(),
    ClientAuthzNull12(),
    ClientAuthzNull12PFS(),
    ClientAuthzOverflow(),
    ClientAuthzOverflow12(),
    ClientAuthzOverflow12PFS(),
    ServerAuthzNull(),
    ServerAuthzNull12(),
    ServerAuthzNull12PFS(),
    ServerAuthzOverflow(),
    ServerAuthzOverflow12(),
    ServerAuthzOverflow12PFS(),
    CertTypeNull(),
    CertTypeNull12(),
    CertTypeNull12PFS(),
    CertTypeOverflow(),
    CertTypeOverflow12(),
    CertTypeOverflow12PFS(),
    SupportedGroupsNull(),
    SupportedGroupsNull12(),
    SupportedGroupsNull12PFS(),
    SupportedGroupsOddLen(),
    SupportedGroupsOddLen12(),
    SupportedGroupsOddLen12PFS(),
    SupportedGroupsOverflow(),
    SupportedGroupsOverflow12(),
    SupportedGroupsOverflow12PFS(),
    ECPointFormatsNull(),
    ECPointFormatsNull12(),
    ECPointFormatsNull12PFS(),
    ECPointFormatsOverflow(),
    ECPointFormatsOverflow12(),
    ECPointFormatsOverflow12PFS(),
    ECPointFormatsCompOnly(),
    ECPointFormatsCompOnly12(),
    ECPointFormatsCompOnly12PFS(),
    SRPNull(),
    SRPNull12(),
    SRPNull12PFS(),
    SRPOverflow(),
    SRPOverflow12(),
    SRPOverflow12PFS(),
    SigAlgsNull(),
    SigAlgsNull12(),
    SigAlgsNull12PFS(),
    SigAlgsOddLen(),
    SigAlgsOddLen12(),
    SigAlgsOddLen12PFS(),
    SigAlgsOverflow(),
    SigAlgsOverflow12(),
    SigAlgsOverflow12PFS(),
    UseSrtpNull(),
    UseSrtpNull12(),
    UseSrtpNull12PFS(),
    UseSrtpOddLen(),
    UseSrtpOddLen12(),
    UseSrtpOddLen12PFS(),
    UseSrtpOverflow(),
    UseSrtpOverflow12(),
    UseSrtpOverflow12PFS(),
    HeartbeatNull(),
    HeartbeatNull12(),
    HeartbeatNull12PFS(),
    HeartbeatInvalid(),
    HeartbeatInvalid12(),
    HeartbeatInvalid12PFS(),
    ALPNNull(),
    ALPNNull12(),
    ALPNNull12PFS(),
    ALPNUnknown(),
    ALPNUnknown12(),
    ALPNUnknown12PFS(),
    ALPNOverflow(),
    ALPNOverflow12(),
    ALPNOverflow12PFS(),
    OCSPv2Null(),
    OCSPv2Null12(),
    OCSPv2Null12PFS(),
    OCSPv2Overflow(),
    OCSPv2Overflow12(),
    OCSPv2Overflow12PFS(),
    SignedCertTSNotNull(),
    SignedCertTSNotNull12(),
    SignedCertTSNotNull12PFS(),
    ClientCertTypeNull(),
    ClientCertTypeNull12(),
    ClientCertTypeNull12PFS(),
    ClientCertTypeOverflow(),
    ClientCertTypeOverflow12(),
    ClientCertTypeOverflow12PFS(),
    ServerCertTypeNull(),
    ServerCertTypeNull12(),
    ServerCertTypeNull12PFS(),
    ServerCertTypeOverflow(),
    ServerCertTypeOverflow12(),
    ServerCertTypeOverflow12PFS(),
    PaddingNull(),
    PaddingNull12(),
    PaddingNull12PFS(),
    Padding300Byte(),
    Padding300Byte12(),
    Padding300Byte12PFS(),
    Padding600Byte(),
    Padding600Byte12(),
    Padding600Byte12PFS(),
    Padding16384Byte(),
    Padding16384Byte12(),
    Padding16384Byte12PFS(),
    Padding16385Byte(),
    Padding16385Byte12(),
    Padding16385Byte12PFS(),
    Padding16387Byte(),
    Padding16387Byte12(),
    Padding16387Byte12PFS(),
    Padding16389Byte(),
    Padding16389Byte12(),
    Padding16389Byte12PFS(),
    Padding17520Byte(),
    Padding17520Byte12(),
    Padding17520Byte12PFS(),
    EtMNotNull(),
    EtMNotNull12(),
    EtMNotNull12PFS(),
    EMSNotNull(),
    EMSNotNull12(),
    EMSNotNull12PFS(),
    CachedInfoNull(),
    CachedInfoNull12(),
    CachedInfoNull12PFS(),
    CachedInfoOverflow(),
    CachedInfoOverflow12(),
    CachedInfoOverflow12PFS(),
    SessionTicketNull(),
    SessionTicketNull12(),
    SessionTicketNull12PFS(),
    SessionTicketOverflow(),
    SessionTicketOverflow12(),
    SessionTicketOverflow12PFS(),
    NPNNotNull(),
    NPNNotNull12(),
    NPNNotNull12PFS(),
    TACKNotNull(),
    TACKNotNull12(),
    TACKNotNull12PFS(),
]


def run_one_probe(ipaddress, port, starttls, specified_probe):
    for probe in probes:
        if specified_probe != type(probe).__name__:
            continue

        logging.info("Probing... %s", type(probe).__name__)
        return {type(probe).__name__: probe.probe(ipaddress, port, starttls)}


def probe(ipaddress, port, starttls):

    results = {}

    for probe in probes:
        logging.info("Probing... %s", type(probe).__name__)
        result = probe.probe(ipaddress, port, starttls)
        results[type(probe).__name__] = result

    return results


def list_probes():
    for probe in probes:
        if type(probe).__doc__ is None:
            print(type(probe).__name__)
        else:
            print("%s: %s" % (type(probe).__name__, type(probe).__doc__))


def probe_strength(db, raw_scores):
    # return how diverse are the expected results of probes in the
    # provided database (which probe is most likely to provide
    # unique fingerprint)
    if raw_scores:
        max_score = max(raw_scores.items(), key=itemgetter(1))
    else:
        max_score = (None, 0)

    # fingerprints that have the same, best, score
    tied_fingerprints = set(
        name for name, val in raw_scores.items() if val == max_score[1]
    )
    probe_matches = {}
    probe_presence = {}
    for fingerprint in db:
        for probe_name, probe_result in fingerprint.probes.items():
            probe_matches.setdefault(probe_name, set()).add(probe_result)
            if probe_name not in probe_presence:
                probe_presence[probe_name] = 0
            if fingerprint.metadata["Description"] in tied_fingerprints:
                probe_presence[probe_name] += 2
            else:
                probe_presence[probe_name] += 1

    max_len = max(len(val) for val in probe_matches.values())
    max_hits = max(probe_presence.values())

    return dict(
        (name, len(val) / max_len * probe_presence.get(name, 0) / max_hits)
        for name, val in probe_matches.items()
    )


def quick_probe(ipaddress, port, starttls, db):
    # try to as quickly as possible reach 10 matching probes
    results = {}
    raw_scores = {}
    best_score = 0
    filtered_db = list(db)

    while True:
        # get list of probes that are most likely to provide unique
        # response from server
        scored_probes = probe_strength(filtered_db, raw_scores)
        probes_iter = (
            name
            for name, _ in sorted(
                scored_probes.items(), key=itemgetter(1), reverse=True
            )
            if name not in results
        )
        # run probes against target until we get at least one match
        for best_probe in probes_iter:
            results.update(run_one_probe(ipaddress, port, starttls, best_probe))

            raw_scores = probe_db.find_raw_matches(db, results)
            if raw_scores:
                break
        else:
            break
        # repeat until the best match has more than 10 matching probes
        best_score = max(raw_scores.items(), key=itemgetter(1))
        if best_score[1] >= 10:
            break
        # in next iteration look for best probes given the already matching
        # libraries (to try breaking ties)
        filtered_db = [fp for fp in db if fp.description() in raw_scores]

    return results


def main():
    options = OptionParser(
        usage="%prog server [options]",
        description="A tool to fingerprint SSL/TLS servers",
    )
    options.add_option(
        "-p", "--port", type="int", default=443, help="TCP port to test (default: 443)"
    )
    options.add_option(
        "-m",
        "--matches",
        dest="matches",
        type="int",
        default=0,
        help=(
            "Only display the first N matching scores"
            "(default: 0 which displays them all)"
        ),
    )
    options.add_option(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="Print debugging messages",
    )
    options.add_option(
        "-s",
        "--starttls",
        dest="starttls",
        type="choice",
        action="store",
        default="auto",
        choices=["auto", "smtp", "ftp", "pop3", "imap", "none"],
        help=(
            "Enable a starttls mode. "
            "The available modes are: auto, smtp, ftp, pop3, imap, none"
        ),
    )
    options.add_option(
        "-t", "--probe", dest="probe", type="string", help="Run the specified probe"
    )
    options.add_option(
        "-a",
        "--add",
        dest="add",
        type="string",
        help="Add the specified fingerprint to the database",
    )
    options.add_option(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        help="List the fingerprints of the target",
    )
    options.add_option(
        "--list-probes",
        dest="list_probes",
        action="store_true",
        help="List the available probes",
    )
    options.add_option(
        "-n",
        "--thorough",
        dest="thorough",
        action="store_true",
        help="Run all probes against target, don't perform a " "quick scan",
    )
    options.add_option(
        "-v",
        "--version",
        dest="version",
        action="store_true",
        help="Display the version information",
    )

    opts, args = options.parse_args()

    if opts.version:
        print("TLS Prober version %s, %s <%s>" % (__version__, __author__, __email__))
        return

    if opts.list_probes:
        list_probes()
        return

    if len(args) < 1:
        options.print_help()
        return

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Probe the server
    if opts.probe:
        results = run_one_probe(args[0], opts.port, opts.starttls, opts.probe)
    elif opts.add or opts.thorough:
        results = probe(args[0], opts.port, opts.starttls)
    else:
        print("Running quick scan, results may be unreliable...")
        db = probe_db.read_database()
        results = quick_probe(args[0], opts.port, opts.starttls, db)

    # Add a fingerprint to the db
    if opts.add:
        filename = probe_db.add_fingerprint(opts.add, results)
        print("Added %s to the database" % opts.add)
        print("The fingerprint is located at:", filename)
        print("Please submit your new fingerprint for inclusion in the next release!")
        return

    # Print the results of the probe
    if opts.list:
        for key, val in sorted(results.items()):
            print("%24s:\t%s" % (key, val))
        return

    # Print the matches
    matches = probe_db.find_matches(results)
    count = 0
    prev_score = None
    for server, score in matches:
        if opts.matches:
            if score != prev_score:
                prev_score = score
                count += 1
            if count > opts.matches:
                break

        print("{0:>65}: {1:6.2f}%".format(server, score * 100))


if __name__ == "__main__":
    main()
