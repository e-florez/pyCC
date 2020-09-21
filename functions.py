

def start ():
  """
   Get path and .xyz to calculation
  """

if len(sys.argv) <= 1:
  	tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
    tmp_dir = tmp_dir.strip()

    if tmp_dir == '.' or len(tmp_dir) < 1:
        working_dir = os.getcwd()
    else:
        working_dir = os.getcwd() + '/' + tmp_dir
else:
    working_dir = os.getcwd() + '/' + sys.argv[1]
    print(f'\nWorking directiry: {working_dir}')

# Check if the working dir exists
if os.path.exists(working_dir) :
    # Change the current working Directory
    os.chdir(working_dir)
else:
    print(f'\n*** ERROR ***')
    exit(f"Can't change the Working Directory, {working_dir} doesn't exist")
