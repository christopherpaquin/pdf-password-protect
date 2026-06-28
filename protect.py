import sys
import os
import secrets
import string

try:
    import pikepdf
except ImportError:
    print("Error: pikepdf is not installed. Run: pip install pikepdf")
    sys.exit(1)


PASSWORD_CHARS = string.ascii_letters + string.digits + "@-_=+."


def generate_password():
    length = secrets.choice(range(8, 11))
    return "".join(secrets.choice(PASSWORD_CHARS) for _ in range(length))


def main():
    if len(sys.argv) != 2:
        print("Usage: python protect.py /path/to/directory")
        sys.exit(1)

    input_dir = os.path.abspath(sys.argv[1])

    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)

    pdf_files = sorted(
        f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")
    )

    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'.")
        sys.exit(0)

    parent_dir = os.path.dirname(input_dir)
    input_name = os.path.basename(input_dir)
    output_dir = os.path.join(parent_dir, input_name + "_password_protected")

    if os.path.exists(output_dir):
        print(f"Warning: Output directory already exists: '{output_dir}'")
        answer = input("Output directory already exists. Overwrite? (yes/no): ").strip()
        if answer != "yes":
            print("Exiting without modifying anything.")
            sys.exit(0)
    else:
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error: Could not create output directory '{output_dir}': {e}")
            sys.exit(1)

    passwords_file = os.path.join(output_dir, "_passwords.txt")
    succeeded = 0
    failed = 0

    for filename in pdf_files:
        print(f"Processing {filename}...", end=" ")
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        password = generate_password()

        try:
            with pikepdf.open(input_path) as pdf:
                pdf.save(
                    output_path,
                    encryption=pikepdf.Encryption(
                        owner=password,
                        user=password,
                        R=6,
                    ),
                )
            with open(passwords_file, "a") as pf:
                pf.write(f"{filename} | {password}\n")
            print("done")
            succeeded += 1
        except Exception as e:
            print(f"ERROR - {e}")
            failed += 1

    print(f"\nSummary: {succeeded} succeeded, {failed} failed.")
    print(f"Output directory : {output_dir}")
    print(f"Passwords file   : {passwords_file}")


if __name__ == "__main__":
    main()
