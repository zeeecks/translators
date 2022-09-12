import os, glob, shutil
import json
import re

# create "repo" directory if not exists
dir = 'repo'
if not os.path.exists(dir):
  os.makedirs(dir)
  print("The new directory is created!")

# delete contents of repo directory
for files in os.listdir(dir):
  path = os.path.join(dir, files)
  try:
      shutil.rmtree(path)
  except OSError:
      os.remove(path)

# # get all translator js files
# files = glob.glob("translators/*.js")
# print(files)

# metadata goes here
metadata = []
denylist = []
for filename in glob.glob("translators/*.js"):
  with open(filename) as file:
    contents = file.read()
  print("Processing " + filename)
  regex_str = r"\{\n(.*?)\}\n"
  meta_string = re.search(regex_str, contents, re.MULTILINE | re.DOTALL)[0]
  meta = json.loads(meta_string)
  translatorID = meta.get("translatorID", None)
  
  if translatorID == None:
    continue

  # between "	***** END LICENSE BLOCK *****\n*/" and "/** BEGIN TEST CASES **/"
  try:
    script = contents.split("***** END LICENSE BLOCK *****\n*/")[1].strip().split("/** BEGIN TEST CASES **/")[0].strip()
    with open(f"repo/{translatorID}", "w") as outfile:
      outfile.write(script)
    metadata.append(str(json.loads(meta_string)))  
  except:
    try:
      script = contents.split("\"\n}\n")[1].strip().split("/** BEGIN TEST CASES **/")[0].strip()
      with open(f"repo/{translatorID}", "w") as outfile:
        outfile.write(script)
      metadata.append(str(json.loads(meta_string)))
    except:
      print("No script detected in \"" + filename + "\"")
      denylist.append(filename.split("/")[1])
denylist.sort()

with open(f"repo/metadata", "w") as outfile:
  outfile.write("[")
  for i in range(len(metadata)):
    metadata_entry = metadata[i]
    outfile.write(metadata_entry)
    if i < len(metadata) - 1:
      outfile.write(",\n")
  outfile.write("]")

print(str(denylist))
print(len(denylist), len(metadata), len(glob.glob("repo")) - 1, len(glob.glob("translators/*.js")))