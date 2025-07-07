Python 3.5.3 (v3.5.3:1880cb95a742, Jan 16 2017, 15:51:26) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> def align_coordinates(pdb_file, output_file):
    with open(pdb_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # 提取原子编号、名称和坐标值
                atom_number = line[6:11].strip()
                atom_name = line[12:16].strip()
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                # 格式化坐标，并写入新文件
                new_line = f"{line[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{line[54:]}"
                outfile.write(new_line)
            else:
                # 对于非 ATOM 或 HETATM 行，直接复制
                outfile.write(line)
# 调用示例
pdb_file = 'ligand.pdb'
output_file = 'ligand_reorder.pdb'
reorder_pdb_atoms(pdb_filename, output_filename)
