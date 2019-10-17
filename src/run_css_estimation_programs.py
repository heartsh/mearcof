#! /usr/bin/env python

import utils
from Bio import SeqIO
import numpy
import seaborn
from matplotlib import pyplot
import os
import multiprocessing
import time
import datetime
import shutil
from Bio import AlignIO

def main():
  (current_work_dir_path, asset_dir_path, program_dir_path, conda_program_dir_path) = utils.get_dir_paths()
  num_of_threads = multiprocessing.cpu_count()
  rnafamprob_dir_path = asset_dir_path + "/rnafamprob"
  mafft_ginsi_dir_path = asset_dir_path + "/mafft_ginsi"
  mafft_xinsi_dir_path = asset_dir_path + "/mafft_xinsi"
  ref_sa_dir_path = asset_dir_path + "/ref_sas"
  mafft_ginsi_plus_neoalifold_dir_path = asset_dir_path + "/mafft_ginsi_plus_neoalifold"
  mafft_xinsi_plus_neoalifold_dir_path = asset_dir_path + "/mafft_xinsi_plus_neoalifold"
  ref_sa_plus_neoalifold_dir_path = asset_dir_path + "/ref_sa_plus_neoalifold"
  mafft_ginsi_plus_centroidalifold_dir_path = asset_dir_path + "/mafft_ginsi_plus_centroidalifold"
  mafft_xinsi_plus_centroidalifold_dir_path = asset_dir_path + "/mafft_xinsi_plus_centroidalifold"
  ref_sa_plus_centroidalifold_dir_path = asset_dir_path + "/ref_sa_plus_centroidalifold"
  if not os.path.isdir(rnafamprob_dir_path):
    os.mkdir(rnafamprob_dir_path)
  if not os.path.isdir(mafft_ginsi_dir_path):
    os.mkdir(mafft_ginsi_dir_path)
  if not os.path.isdir(mafft_xinsi_dir_path):
    os.mkdir(mafft_xinsi_dir_path)
  if not os.path.isdir(ref_sa_dir_path):
    os.mkdir(ref_sa_dir_path)
  if not os.path.isdir(mafft_ginsi_plus_neoalifold_dir_path):
    os.mkdir(mafft_ginsi_plus_neoalifold_dir_path)
  if not os.path.isdir(mafft_xinsi_plus_neoalifold_dir_path):
    os.mkdir(mafft_xinsi_plus_neoalifold_dir_path)
  if not os.path.isdir(ref_sa_plus_neoalifold_dir_path):
    os.mkdir(ref_sa_plus_neoalifold_dir_path)
  if not os.path.isdir(mafft_ginsi_plus_centroidalifold_dir_path):
    os.mkdir(mafft_ginsi_plus_centroidalifold_dir_path)
  if not os.path.isdir(mafft_xinsi_plus_centroidalifold_dir_path):
    os.mkdir(mafft_xinsi_plus_centroidalifold_dir_path)
  if not os.path.isdir(ref_sa_plus_centroidalifold_dir_path):
    os.mkdir(ref_sa_plus_centroidalifold_dir_path)
  rna_seq_dir_path = asset_dir_path + "/sampled_rna_fams"
  bpap_mat_file = "bpap_mats.dat"
  upp_mat_file = "upp_mats.dat"
  gammas = [2. ** i for i in range(-7, 11)]
  mafft_ginsi_plus_centroidalifold_params = []
  mafft_xinsi_plus_centroidalifold_params = []
  ref_sa_plus_centroidalifold_params = []
  centroidalifold_params_4_elapsed_time = []
  rnafamprob_and_neoalifold_elapsed_time = 0.
  for rna_seq_file in os.listdir(rna_seq_dir_path):
    if not rna_seq_file.endswith(".fa"):
      continue
    rna_seq_file_path = os.path.join(rna_seq_dir_path, rna_seq_file)
    (rna_familiy_name, extension) = os.path.splitext(rna_seq_file)
    rnafamprob_output_dir_path = os.path.join(rnafamprob_dir_path, rna_familiy_name)
    rnafamprob_command = "rnafamprob -i " + rna_seq_file_path + " -o " + rnafamprob_output_dir_path
    begin = time.time()
    utils.run_command(rnafamprob_command)
    elapsed_time = time.time() - begin
    rnafamprob_and_neoalifold_elapsed_time += elapsed_time
    bpap_mat_file_path = os.path.join(rnafamprob_output_dir_path, bpap_mat_file)
    upp_mat_file_path = os.path.join(rnafamprob_output_dir_path, upp_mat_file)
    mafft_ginsi_output_file_path = os.path.join(mafft_ginsi_dir_path, rna_familiy_name + ".aln")
    mafft_xinsi_output_file_path = os.path.join(mafft_xinsi_dir_path, rna_familiy_name + ".aln")
    run_mafft((rna_seq_file_path, mafft_ginsi_output_file_path, "ginsi"))
    run_mafft((rna_seq_file_path, mafft_xinsi_output_file_path, "xinsi"))
    ref_sa_file_path = os.path.join(ref_sa_dir_path, rna_familiy_name + ".aln")
    mafft_ginsi_plus_neoalifold_output_dir_path = os.path.join(mafft_ginsi_plus_neoalifold_dir_path, "csss_of_" + rna_familiy_name)
    mafft_xinsi_plus_neoalifold_output_dir_path = os.path.join(mafft_xinsi_plus_neoalifold_dir_path, "csss_of_" + rna_familiy_name)
    ref_sa_plus_neoalifold_output_dir_path = os.path.join(ref_sa_plus_neoalifold_dir_path, "csss_of_" + rna_familiy_name)
    mafft_ginsi_plus_centroidalifold_output_dir_path = os.path.join(mafft_ginsi_plus_centroidalifold_dir_path, "csss_of_" + rna_familiy_name)
    mafft_xinsi_plus_centroidalifold_output_dir_path = os.path.join(mafft_xinsi_plus_centroidalifold_dir_path, "csss_of_" + rna_familiy_name)
    ref_sa_plus_centroidalifold_output_dir_path = os.path.join(ref_sa_plus_centroidalifold_dir_path, "csss_of_" + rna_familiy_name)
    if not os.path.isdir(mafft_ginsi_plus_neoalifold_output_dir_path):
      os.mkdir(mafft_ginsi_plus_neoalifold_output_dir_path)
    if not os.path.isdir(mafft_xinsi_plus_neoalifold_output_dir_path):
      os.mkdir(mafft_xinsi_plus_neoalifold_output_dir_path)
    if not os.path.isdir(ref_sa_plus_neoalifold_output_dir_path):
      os.mkdir(ref_sa_plus_neoalifold_output_dir_path)
    if not os.path.isdir(mafft_ginsi_plus_centroidalifold_output_dir_path):
      os.mkdir(mafft_ginsi_plus_centroidalifold_output_dir_path)
    if not os.path.isdir(mafft_xinsi_plus_centroidalifold_output_dir_path):
      os.mkdir(mafft_xinsi_plus_centroidalifold_output_dir_path)
    if not os.path.isdir(ref_sa_plus_centroidalifold_output_dir_path):
      os.mkdir(ref_sa_plus_centroidalifold_output_dir_path)
    for gamma in gammas:
      gamma_str = str(gamma)
      output_file = "gamma=" + gamma_str + ".sth"
      mafft_ginsi_plus_neoalifold_output_file_path = os.path.join(mafft_ginsi_plus_neoalifold_output_dir_path, output_file)
      neoalifold_command = "neoalifold -a " + mafft_ginsi_output_file_path + " -p " + bpap_mat_file_path + " -q " + upp_mat_file_path + " -o " + mafft_ginsi_plus_neoalifold_output_file_path + " --gamma " + gamma_str
      utils.run_command(neoalifold_command)
      mafft_xinsi_plus_neoalifold_output_file_path = os.path.join(mafft_xinsi_plus_neoalifold_output_dir_path, output_file)
      neoalifold_command = "neoalifold -a " + mafft_xinsi_output_file_path + " -p " + bpap_mat_file_path + " -q " + upp_mat_file_path + " -o " + mafft_xinsi_plus_neoalifold_output_file_path + " --gamma " + gamma_str
      begin = time.time()
      utils.run_command(neoalifold_command)
      elapsed_time = time.time() - begin
      if gamma == 1:
        rnafamprob_and_neoalifold_elapsed_time += elapsed_time
      ref_sa_plus_neoalifold_output_file_path = os.path.join(ref_sa_plus_neoalifold_output_dir_path, output_file)
      neoalifold_command = "neoalifold -a " + ref_sa_file_path + " -p " + bpap_mat_file_path + " -q " + upp_mat_file_path + " -o " + ref_sa_plus_neoalifold_output_file_path + " --gamma " + gamma_str
      utils.run_command(neoalifold_command)
      mafft_ginsi_plus_centroidalifold_output_file_path = os.path.join(mafft_ginsi_plus_centroidalifold_output_dir_path, output_file)
      mafft_xinsi_plus_centroidalifold_output_file_path = os.path.join(mafft_xinsi_plus_centroidalifold_output_dir_path, output_file)
      ref_sa_plus_centroidalifold_output_file_path = os.path.join(ref_sa_plus_centroidalifold_output_dir_path, output_file)
      mafft_ginsi_plus_centroidalifold_params.insert(0, (mafft_ginsi_output_file_path, mafft_ginsi_plus_centroidalifold_output_file_path, gamma_str))
      mafft_xinsi_plus_centroidalifold_params.insert(0, (mafft_xinsi_output_file_path, mafft_xinsi_plus_centroidalifold_output_file_path, gamma_str))
      ref_sa_plus_centroidalifold_params.insert(0, (ref_sa_file_path, ref_sa_plus_centroidalifold_output_file_path, gamma_str))
      if gamma == 1:
        centroidalifold_params_4_elapsed_time.insert(0, (mafft_xinsi_output_file_path, mafft_xinsi_plus_centroidalifold_output_file_path, gamma_str))
  pool = multiprocessing.Pool(num_of_threads)
  pool.map(run_centroidalifold, mafft_ginsi_plus_centroidalifold_params)
  pool.map(run_centroidalifold, mafft_xinsi_plus_centroidalifold_params)
  pool.map(run_centroidalifold, ref_sa_plus_centroidalifold_params)
  begin = time.time()
  pool.map(run_centroidalifold, centroidalifold_params_4_elapsed_time)
  centroidalifold_elapsed_time = time.time() - begin
  print("The elapsed time of the RNAfamProb and NeoAliFold programs for a test set = %f [s]." % rnafamprob_and_neoalifold_elapsed_time)
  print("The elapsed time of the CentroidAlifold program for a test set = %f [s]." % centroidalifold_elapsed_time)

def run_mafft(mafft_params):
  (rna_seq_file_path, mafft_output_file_path, mafft_type) = mafft_params
  mafft_command = "mafft-%s " % mafft_type + "--clustalout " + rna_seq_file_path + " > " + mafft_output_file_path
  utils.run_command(mafft_command)

def run_centroidalifold(centroidalifold_params):
  (sa_file_path, centroidalifold_output_file_path, gamma_str) = centroidalifold_params
  centroidalifold_command = "centroid_alifold " + sa_file_path + " -g " + gamma_str
  (output, _, _) = utils.run_command(centroidalifold_command)
  css = str(output).strip().split("\\n")[2].split()[0]
  sta = AlignIO.read(sa_file_path, "clustal")
  AlignIO.write(sta, centroidalifold_output_file_path, "stockholm")
  sta = AlignIO.read(centroidalifold_output_file_path, "stockholm")
  sta.column_annotations["secondary_structure"] = css
  AlignIO.write(sta, centroidalifold_output_file_path, "stockholm")

if __name__ == "__main__":
  main()
