"""Copy original local resources into the new website layout without overwriting files."""
from pathlib import Path
import argparse,json,re,unicodedata,shutil
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('original_folder',type=Path,help='Original website folder containing Icons_Papers, Slides, Teaching, etc.')
parser.add_argument('--dry-run',action='store_true',help='Show destinations without copying')
args=parser.parse_args();source=args.original_folder.expanduser().resolve()
if not source.is_dir():parser.error('Original website folder does not exist')
if source==ROOT:parser.error('Choose the original website folder, not this redesigned folder')
mapping=json.loads((ROOT/'content/resource-map.json').read_text())
def slug(s):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def destination(relative):
 old=relative.as_posix()
 if old in mapping:return mapping[old]
 parts=relative.parts;name=slug(relative.stem)+relative.suffix.lower()
 if parts[0]=='Icons_Papers':return 'assets/images/publications/'+name
 if parts[0]=='Research Summaries':return ('assets/media/research/' if relative.suffix.lower() in ['.mp4','.webm'] else 'assets/images/research/')+'/'.join([slug(x) for x in parts[1:-1]]+[name])
 categories={'CV':'cv','Slides':'presentations','Posters':'posters','Preprints':'preprints','Teaching':'teaching','Software':'software'}
 if parts[0] in categories:return 'downloads/'+categories[parts[0]]+'/'+'/'.join([slug(x) for x in parts[1:-1]]+[name])
 return None
files=[]
for name in ['Icons_Papers','Research Summaries','CV','Slides','Posters','Preprints','Teaching','Software']:
 folder=source/name
 if folder.is_dir():files.extend(p for p in folder.rglob('*') if p.is_file() and not any(x.startswith('.') for x in p.relative_to(source).parts))
if (source/'Photo.jpg').is_file():files.append(source/'Photo.jpg')
copied=skipped=0;destinations={}
for file in sorted(files):
 relative=file.relative_to(source);new=destination(relative)
 if not new:continue
 if new in destinations:raise SystemExit(f'Destination collision: {relative} and {destinations[new]} both become {new}')
 destinations[new]=relative;target=ROOT/new
 if target.exists():skipped+=1;continue
 print(f'{relative} -> {new}')
 if not args.dry_run:target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,target)
 copied+=1
print(f'{copied} files {"would be copied" if args.dry_run else "copied"}; {skipped} existing files left unchanged.')
if not files:print('No resource files found. Check that you selected the original website folder.')
