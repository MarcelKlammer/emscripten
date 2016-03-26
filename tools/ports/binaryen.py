import os, shutil, logging, subprocess, multiprocessing

TAG = 'version_1'

def needed(settings, shared):
  if not settings.BINARYEN: return False
  try:
    if shared.BINARYEN_ROOT: # if defined, and not falsey, we don't need the port
      logging.debug('binaryen root already set to ' + shared.BINARYEN_ROOT)
      return False
  except:
    pass
  return True

def get(ports, settings, shared):
  if not needed(settings, shared):
    return []
  ports.fetch_project('binaryen', 'https://github.com/WebAssembly/binaryen/archive/' + TAG + '.zip', 'binaryen-' + TAG)
  def create():
    logging.warning('building port: binaryen')
    # TODO: refactor into Ports.build_native()?
    old = os.getcwd()
    try:
      os.chdir(os.path.join(ports.get_dir(), 'binaryen', 'binaryen-' + TAG))
      subprocess.check_call(['cmake', '.'])
      subprocess.check_call(['make', '-j', os.environ.get('EMCC_CORES') or str(multiprocessing.cpu_count())])
    finally:
      os.chdir(old)
    # the "output" of this port build is a tag file, saying which port we have
    tag_file = os.path.join(ports.get_dir(), 'binaryen', 'tag.txt')
    open(tag_file, 'w').write(TAG)
    return tag_file
  return [shared.Cache.get('binaryen-tag', create, what='port', extension='.txt')]

def process_args(ports, args, settings, shared):
  if not needed(settings, shared):
    return args
  get(ports, settings, shared)
  shared.BINARYEN_ROOT = os.path.join(ports.get_dir(), 'binaryen', 'binaryen-' + TAG)
  logging.debug('setting binaryen root to ' + shared.BINARYEN_ROOT)
  return args

def show():
  return 'Binaryen (Apache 2.0 license)'

