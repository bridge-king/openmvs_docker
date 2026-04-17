import os
import glob
import stat
import shutil
import argparse
import subprocess


def run_openmvs_commands(args):
    accepted_apps = ["InterfaceCOLMAP", "DensifyPointCloud", "ReconstructMesh", "RefineMesh", "TextureMesh"]

    if args.output_point_cloud_file is not None:
        os.makedirs(os.path.dirname(args.output_point_cloud_file), exist_ok=True)
    if args.output_mesh_dir is not None:
        os.makedirs(args.output_mesh_dir, exist_ok=True)

    os.chdir(args.workdir_path)

    commands_run = []
    run_mesh_generation = False

    commands = args.commands.split(';')

    for cmd0 in commands:
        cmd = cmd0.strip()
        cmd_fields = cmd.split(' ')
        app_name = cmd_fields[0]

        if app_name in accepted_apps:
            if app_name == "ReconstructMesh":
                run_mesh_generation = True
                n_dmaps = len(glob.glob("depth*.dmap"))

                if args.min_num_images_for_meshing is not None:
                    if n_dmaps < args.min_num_images_for_meshing:
                        print("---")
                        print(f"The number of generated depth maps ({n_dmaps}) is lower than required ({args.min_num_images_for_meshing}). Skip mesh generation steps.")
                        run_mesh_generation = False
                        break

            if app_name == "TextureMesh":
                for k in range(len(cmd_fields)):
                    if cmd_fields[k] in ["-o", "--output-file"]:
                        output_mesh_name = os.path.splitext(cmd_fields[k + 1])[0]

            try:
                subprocess.run(cmd_fields, check=True)
                commands_run += [cmd]
            except subprocess.CalledProcessError as error:
                print(f"The following command failed with exit code {error.returncode}: {cmd}")

        elif app_name != "":
            raise ValueError(f"Unsupported app: {app_name}")

    for fn in glob.glob("*"):
        current_mode = os.stat(fn).st_mode
        os.chmod(fn, current_mode | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    # Assuming the output point cloud file in the work dir is scene_dense.ply
    if args.output_point_cloud_file is not None:
        if os.path.exists("scene_dense.ply"):
            shutil.copy("scene_dense.ply", args.output_point_cloud_file)

    if run_mesh_generation and args.output_mesh_dir is not None:
        for fn in glob.glob(output_mesh_name + "*"):
            shutil.copy(fn, args.output_mesh_dir)

    print("======")
    print("Finished running OpenMVS commands:")
    for cmd in commands_run:
        print("  " + cmd)
    print("")
    if os.path.exists(args.output_point_cloud_file):
        print(f"Copied output point cloud file to {args.output_point_cloud_file}")
    if run_mesh_generation and os.path.exists(os.path.join(args.output_mesh_dir, output_mesh_name + ".ply")):
        print(f"Copied output mesh files {output_mesh_name}* to {args.output_mesh_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--workdir_path", required=True, help="absolute path to work dir, which contains input data in 'dense' subdir")
    parser.add_argument("-c", "--commands", required=True, help="OpenMVS commands to run, separated by ;")

    parser.add_argument("-n", "--min_num_images_for_meshing", type=int, help="minimum number of images for mesh generation")

    parser.add_argument("-p", "--output_point_cloud_file", help="absolute path to output point cloud file (.ply)")
    parser.add_argument("-m", "--output_mesh_dir", help="absolute path to output dir for mesh files (.ply and .png)")

    args_main = parser.parse_args()

    try:
        run_openmvs_commands(args_main)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
