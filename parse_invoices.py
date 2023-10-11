# %%
import os
import sys
import argparse
import pdftotext


def rename_invoice(
        fname: str,
        data_dir: str = '~/github/lawn_care_invoices/data',
        source_subdir: str = 'raw',
        dest_subdir: str = 'interim'
) -> None:
    """
    Rename the specified invoice based on its invoice number.

    This function reads the content of the specified invoice file, extracts the invoice number, and then renames the file using the format "Invoice-<Invoice Number>.pdf".

    Args:
        fname (str): The filename of the invoice to be renamed.
        data_dir (str, optional): The root directory where invoice files are located.
            Defaults to '~/github/lawn_care_invoices/data/'.
        source_subdir (str, optional): The subdirectory within 'data_dir' where the raw 
            invoice files are located. Defaults to 'raw'.
        dest_subdir (str, optional): The subdirectory within 'data_dir' where the   
            renamed invoices should be saved. Defaults to 'interim'.

    Returns:
        None: The original invoice is renamed and saved in the source_subdir.

    Requires:
        - os
        - pdftotext

    Examples:
        >>> rename_invoice("sample_invoice.pdf")
        This will rename 'sample_invoice.pdf' based on its invoice number and save it
        in the 'interim' subdirectory of '~/github/lawn_care_invoices/data/'.

    Note:
        The function assumes that the first instance of the word 'Invoice' followed by a space and then a number, on the first page of the PDF, is the invoice number. If the invoice doesn't follow this pattern, the function might not work as expected.
    """

    data_dir = os.path.expanduser(data_dir)
    input_path = f'{data_dir}/{source_subdir}/{fname}'

    with open(input_path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    matches = (
        line for line in iter(pdf[0].split('\n'))
        if line[:7] == 'Invoice'
    )
    first_match = next(matches)
    invoice_number = first_match.split(' ')[1]

    fname_out = f'Invoice-{invoice_number}.pdf'
    output_path = f'{data_dir}/{dest_subdir}/{fname_out}'
    copy_and_rename = f'cp {input_path} {output_path}'

    return os.system(copy_and_rename)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--rename', action='store_true', help='Copy invoice')
    parser.add_argument('fname', help='file name of PDF to be processed')
    args = parser.parse_args()

    if args.rename:
        rename_invoice(args.fname)
