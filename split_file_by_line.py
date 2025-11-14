import os
import sys


def split_file(input_file, lines_per_file=500):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    base_name, ext = os.path.splitext(input_file)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file '{input_file}': {e}")
        return

    total_lines = len(lines)
    print(f"File '{input_file}' has {total_lines} lines.")

    for i in range(0, total_lines, lines_per_file):
        end_index = min(i + lines_per_file, total_lines)

        start_line = i + 1
        output_file = f"{base_name}_{start_line}{ext}"

        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.writelines(lines[i:end_index])

        print(f"Created '{output_file}' with lines {start_line} to {end_index}")

    print(
        f"Split completed. Created {len(lines) // lines_per_file + (1 if len(lines) % lines_per_file else 0)} files."
    )


split_file("./english.csv")
split_file("./chinese_traditional.csv")