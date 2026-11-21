import os
import glob

# Clean up temporary scripts
scripts_dir = 'D:\\Project-Fremen\\backend\\scripts'
backend_dir = 'D:\\Project-Fremen\\backend'

for f in glob.glob(os.path.join(scripts_dir, 'add_*.py')):
    os.remove(f)
    print(f'Deleted: {f}')

for f in glob.glob(os.path.join(scripts_dir, 'fix_*.py')):
    os.remove(f)
    print(f'Deleted: {f}')

for f in glob.glob(os.path.join(scripts_dir, 'check_*_dups.py')):
    os.remove(f)
    print(f'Deleted: {f}')

for f in glob.glob(os.path.join(scripts_dir, 'check_dup_ids.py')):
    os.remove(f)
    print(f'Deleted: {f}')

for f in glob.glob(os.path.join(backend_dir, 'debug_*.py')):
    os.remove(f)
    print(f'Deleted: {f}')

for f in glob.glob(os.path.join(backend_dir, 'final_state.py')):
    os.remove(f)
    print(f'Deleted: {f}')

print('Cleanup complete.')