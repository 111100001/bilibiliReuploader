import os

# Define the input file path
input_file_path = '/home/ubuntu/links/grouped.txt'

# Create a directory to store the output files
output_dir = '/home/ubuntu/links/streams'
os.makedirs(output_dir, exist_ok=True)

# Initialize variables
current_stream = 0
stream_links = []

# Read the input file
with open(input_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('Stream'):
            # Save the previous stream links to a file
            if current_stream and stream_links:
                output_file_path = os.path.join(output_dir, f'{current_stream}.txt')
                with open(output_file_path, 'w') as output_file:
                    output_file.write('\n'.join(stream_links))
            
            # Start a new stream
            current_stream += 1
            stream_links = []
        elif line:
            # Add the link to the current stream
            stream_links.append(line)

    # Save the last stream links to a file
    if current_stream and stream_links:
        output_file_path = os.path.join(output_dir, f'{current_stream}.txt')
        with open(output_file_path, 'w') as output_file:
            output_file.write('\n'.join(stream_links))