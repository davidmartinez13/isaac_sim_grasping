sudo chmod -R 777 /home/$USER/f3rm/datasets/eyeinhand_nerf1/benchmark
~/.local/share/ov/pkg/isaac-sim-2023.1.0-hotfix.1/python.sh ./standalone_benchmark.py \
    --json_dir=/home/$USER/f3rm/datasets/eyeinhand_nerf1/benchmark \
    --gripper_dir=/home/$USER/isaac_sim_grasping/grippers \
    --objects_dir=/home/$USER/isaac_sim_grasping/gazebo-objects/objects_gazebo/ycb \
    --output_dir=/home/$USER/Documents/Dataset/hithand_filtered \
    --num_w=50 \
    --test_time=3 \
    --controller=default \
    --print_results \
    --/log/level=error \
    --/log/fileLogLevel=error \
    --/log/outputStreamLevel=error