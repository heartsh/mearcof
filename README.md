# Consensus Secondary Structure Predictor Engaging Structural Alignment-based Error Correction
# Installation
This project is written mainly in Rust, a systems programming language.
You need to install Rust components, i.e., rustc (the Rust compiler), cargo (the Rust package manager), and the Rust standard library.
Visit [the Rust website](https://www.rust-lang.org) to see more about Rust.
You can install Rust components with the following one line:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
The above installation is done by [Rustup](https://github.com/rust-lang-nursery/rustup.rs), and Rustup enables to easily switch a compiler in use.
As ConsAlifold's dependencies, you need to install [ViennaRNA](https://www.tbi.univie.ac.at/RNA/) and [LocARNA-P](https://github.com/s-will/LocARNA) (if you wish to use instead of [ConsProb](https://github.com/heartsh/consprob)).
You can install ConsAlifold as follows: 
```bash
# AVX, SSE, and MMX enabled for rustc
# Another example: RUSTFLAGS='--emit asm -C target-feature=+avx2 -C target-feature=+ssse3 -C target-feature=+mmx -C target-feature=+fma'
RUSTFLAGS='--emit asm -C target-feature=+avx -C target-feature=+ssse3 -C target-feature=+mmx' \
  cargo install consalifold
```
Check if you have installed ConsAlifold properly as follows:
```bash
# Its available command options will be displayed.
consalifold
```
You can run ConsAlifold with a prepared test RNA alignment:
```bash
git clone https://github.com/heartsh/consalifold \
  && cd consalifold
cargo test --release
# The below command requires Gnuplot (http://www.gnuplot.info)
# Benchmark results will be found at "./target/criterion/report/index.html"
cargo bench
```
By the following Python script, you can reproduce the figures shown in [the paper describing ConsAlifold's principle](https://doi.org/10.1093/bioinformatics/btab738):
```bash
cd scripts
# Please install python packages required to this reproduction.
# Saved figures will appear at the "../assets/images" directory.
./run_all.sh
```

# Docker Playground <img src="./assets/images_fixed/docker_logo.png" width="40">
I offer [my Docker-based playground for RNA software and its instruction](https://github.com/heartsh/rna-playground) to replay my computational experiments easily.

# Method Digest
[RNAalifold](https://www.tbi.univie.ac.at/RNA/) folds each RNA sequence alignment, minimizing the average free energy of a predicted consensus secondary structure.
Based on posterior column base-pairing probabilities on RNA consensus secondary structures, [PETfold](https://rth.dk/resources/petfold/) and [CentroidAlifold](https://github.com/satoken/centroid-rna-package) fold each RNA sequence alignment.
PETfold and CentroidAlifold correct potential errors in each input sequence alignment utilizing posterior nucleotide base-pairing probabilities on RNA secondary structures.
To achieve better alignment error correction than PETfold and CentroidAlifold, I developed ConsAlifold implemented in this repository.
ConsAlifold folds each RNA sequence alignment correcting its potential errors with average probabilistic consistency.

# Author
[Heartsh](https://github.com/heartsh)

# License
Copyright (c) 2018 Heartsh  
Licensed under [the MIT license](http://opensource.org/licenses/MIT).
