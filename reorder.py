def reorder_pdb_atoms(pdb_filename, output_filename):
    with open(pdb_filename, 'r') as pdb_file:
        lines = pdb_file.readlines()

    atom_counter = 1  # 原子编号从1开始
    residue_counter = 0  # 氨基酸序号从1开始
    last_residue = None
    reordered_lines = []

    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            # 提取原子信息
            atom_serial = line[6:11].strip()  # 原子序号
            residue_name = line[17:20].strip()  # 氨基酸名称
            residue_seq = int(line[23:26].strip())  # 氨基酸序号
            
            # 如果氨基酸序号改变，重新编号
            if residue_seq != last_residue:
                residue_counter += 1
                last_residue = residue_seq

            # 更新原子序号
            atom_line = (
                line[:6] + f"{atom_counter:5d}" + line[11:22] + f"{residue_counter:4d}" + line[26:]
            )
            reordered_lines.append(atom_line)

            atom_counter += 1  # 继续下一个原子的编号
        else:
            # 如果不是原子行（如TER、其他信息行），不做更改
            reordered_lines.append(line)

    with open(output_filename, 'w') as output_file:
        output_file.writelines(reordered_lines)

    print(f"Reordering complete. Output saved to {output_filename}.")

# 调用示例
pdb_filename = 'protein.pdb'
output_filename = 'protein_reorder.pdb'
reorder_pdb_atoms(pdb_filename, output_filename)

