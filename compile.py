import os
import subprocess
import sys
import argparse
import shutil
from PIL import Image  # Import Pillow for image handling

def run_command(command, error_message, debug=False):
    """Run a system command and exit if it fails. Optionally print the command if in debug mode."""
    if debug:
        print(f'Debug: Running command -> {command}')
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        print(error_message)
        sys.exit(1)

def convert_png_to_ico(png_file, output_ico):
    """Convert a PNG file to ICO format."""
    try:
        img = Image.open(png_file)
        img.save(output_ico, format='ICO')
        print(f'Success: Converted {png_file} to {output_ico}')
    except Exception as e:
        print(f'Error: Failed to convert PNG to ICO - {e}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Batch file to Python conversion')
    parser.add_argument('script', help='Python script file to compile')
    parser.add_argument('-o', '--output', default='output', help='Output directory (default: output)')
    parser.add_argument('-i', '--icon', help='Icon file (PNG or ICO)')
    parser.add_argument('-v', '--version', help='Python version (e.g., 313) or path to Python installation')
    parser.add_argument('-l', '--library', help='Python library version (e.g., 313)')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode to print commands')

    args = parser.parse_args()
    debug_mode = args.debug

    # Check if the script file exists
    script = args.script
    if not os.path.isfile(script):
        print(f'Error: The script file "{script}" does not exist.')
        sys.exit(1)

    # Determine Python include and libs based on version or path
    if args.version:
        if os.path.isdir(args.version):
            # If -v is a directory path, use it as Python installation directory
            python_include = os.path.join(args.version, 'include')
            python_libs = os.path.join(args.version, 'libs')
            
            if not args.library:
                print('Error: When specifying a custom Python path, the library version (-l) must be provided.')
                sys.exit(1)
            python_library = f'-lpython{args.library}'
        else:
            # If -v is a version number, assume default path structure
            python_include = f'C:\\Program Files\\Python{args.version}\\include'
            python_libs = f'C:\\Program Files\\Python{args.version}\\libs'
            python_library = f'-lpython{args.version}'
            if args.library:
                python_library = f"-lpython{args.library}"
    else:
        # Default to Python 3.13 if no version specified
        python_include = r'C:\Program Files\Python313\include'
        python_libs = r'C:\Program Files\Python313\libs'
        python_library = '-lpython313'

    # Extract filename without extension
    filename = os.path.splitext(os.path.basename(script))[0]
    newfile = f'{filename}.exe'
    newfile2 = f'{filename}.cpp'

    # Set the output directory
    outputdir = args.output
    if not os.path.exists(outputdir):
        print(f'Output directory "{outputdir}" does not exist. Creating it.')
        os.makedirs(outputdir)

    # Generate C++ code using Cython (check if cython is available)
    cython_command = f'cython --embed -+ --line-directives --3str --annotate-fullc "{script}"'
    run_command(cython_command, 'Error: Cython compilation failed.', debug=debug_mode)

    iconobj = ''
    if args.icon:
        iconfile = args.icon
        if not os.path.isfile(iconfile):
            print(f'Error: The icon file "{iconfile}" does not exist.')
            sys.exit(1)
        
        # Check if the icon file is a PNG, and convert to ICO if necessary
        if iconfile.lower().endswith('.png'):
            ico_file = 'temp_icon.ico'
            convert_png_to_ico(iconfile, ico_file)
            iconfile = ico_file
        
        # Create a temporary resource file for the icon
        with open('temp_icon.rc', 'w') as f:
            f.write(f'IDI_ICON1 ICON "{iconfile}"')
        
        # Compile the resource file into an object file
        run_command('windres temp_icon.rc -o temp_icon.o', 'Error: Windres compilation failed.', debug=debug_mode)
        os.remove('temp_icon.rc')
        iconobj = 'temp_icon.o'
    
    # Compile with g++
    gpp_command = (
        f'g++ "{newfile2}" -o "{outputdir}\\{newfile}" -I"{python_include}" -L"{python_libs}" '
        f'{iconobj} {python_library} -static-libgcc -static-libstdc++ -municode'
    )
    
    # Print the g++ command if debug mode is enabled
    run_command(gpp_command, f'Error: g++ compilation failed {"with icon" if iconobj else "without icon"}.', debug=debug_mode)

    # Clean up temporary files
    if iconobj:
        os.remove(iconobj)
    if os.path.isfile(newfile2):
        os.remove(newfile2)
    if os.path.isfile('temp_icon.ico'):
        os.remove('temp_icon.ico')

    print(f'Success: {newfile} has been created in "{outputdir}".')

if __name__ == '__main__':
    main()
