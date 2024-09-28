import json
import os

# Define the input JSON file and output MGF file
input_file = 'data.json'
output_file = 'data.mgf'

# Function to convert HRMS data to MGF format
def generate_mgf(data):
    mgf_content = []

    for scan in data['fullscan']:
        if scan['ms_ms_available'] == "Yes":
            # Generate the FEATURE_ID based on "mz" and "rt_minutes"
            feature_id = f"{scan['mz']}_{scan['rt_minutes']}"
            rt_in_seconds = scan['rt_minutes'] * 60  # Convert minutes to seconds

            # Start building the MGF block
            mgf_block = []
            mgf_block.append("BEGIN IONS")
            mgf_block.append(f"FEATURE_ID={feature_id}")
            mgf_block.append("MSLEVEL=2")
            mgf_block.append(f"RTINSECONDS={rt_in_seconds:.2f}")
            mgf_block.append(f"PEPMASS={scan['mz']}")
            mgf_block.append("CHARGE=1+")
            mgf_block.append(f"SCANS={data['sample_id']}")  # You can modify how SCANS are set
            mgf_block.append(f"Num peaks={len(scan['hrmsms_mz'])}")

            # Add m/z and intensity pairs (from hrmsms_mz and hrmsms_int)
            for mz, intensity in zip(scan['hrmsms_mz'], scan['hrmsms_int']):
                mgf_block.append(f"{mz} {intensity}")

            mgf_block.append("END IONS\n")  # End the block
            mgf_content.append("\n".join(mgf_block))

    return "\n\n".join(mgf_content)  # Separate blocks with empty lines

# Read the JSON data
with open(input_file, 'r') as f:
    data = json.load(f)

# Generate the MGF content from the JSON data
mgf_data = generate_mgf(data)

# Write the MGF content to an output file
with open(output_file, 'w') as f:
    f.write(mgf_data)

print(f"MGF file has been generated at: {os.path.abspath(output_file)}")
