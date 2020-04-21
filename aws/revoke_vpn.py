#!/usr/bin/env python3
import sys
import boto3


def main(name):
    acm = boto3.client("acm")
    pca_client = boto3.client("acm-pca")  # ACM Private CA client

    certs = []
    cert_results = acm.list_certificates()
    certs += cert_results["CertificateSummaryList"]
    nextToken = cert_results.get("NextToken", None)
    # Retrive all certs
    while nextToken != None:
        cert_results = acm.list_certificates(
            NextToken=nextToken
        )  # Get next set of certs
        certs += cert_results["CertificateSummaryList"]  # Add to list of certs
        nextToken = cert_results.get("NextToken", None)  # Get nextToken if avail

    # Search through the certs
    user_certs = [x for x in certs if x["DomainName"].find(name) != -1]
    if len(user_certs) == 0:
        print(f"No certificates found for {name}")
        return -1

    # present choice of certs to user
    for i, cert in enumerate(user_certs):
        print(f"[{i}]: {cert['DomainName']}")

    disp_string = "" if len(user_certs) == 1 else f"-{len(user_certs) - 1}"
    choice = input(f"Certificate to delete [0{disp_string}]: ")
    choice = int(choice)

    chosen_cert = user_certs[choice]["CertificateArn"]
    cert_serial = acm.describe_certificate(CertificateArn=chosen_cert)["Certificate"][
        "Serial"
    ]

    # Only retrieves the first Private CA, which could be an issue if an org has multiple
    private_ca_arn = pca_client.list_certificate_authorities()[
        "CertificateAuthorities"
    ][0]["Arn"]

    # Revoke certificate with $SERIAL
    already_revoked = False
    print(f"Revoking certificate for {name} with serial {cert_serial}")
    try:
        print(
            pca_client.revoke_certificate(
                CertificateAuthorityArn=private_ca_arn,
                CertificateSerial=cert_serial,
                RevocationReason="CESSATION_OF_OPERATION",
            )
        )
    except pca_client.exceptions.RequestAlreadyProcessedException:
        print("Certificate has already been revoked")
        already_revoked = True

    if not already_revoked:
        choice = input(f"Delete certificate from AWS? [y/N]: ")
    else:
        choice = "n"

    # Delete certificate?
    choice = input(f"Delete certificate from AWS? [y/N]: ")
    if "y" in choice:
        acm.delete_certificate(CertificateArn=chosen_cert)
        print(f"Deleted {cert_serial}")
    else:
        print(f"Did not delete {cert_serial}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"Revoke a user's certificate\n\tusage: {sys.argv[0]} user-name")
