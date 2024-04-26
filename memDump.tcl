foreach hardware_name [get_hardware_names] {
	set hw_name $hardware_name
}

foreach device_name [get_device_names -hardware_name $hw_name] {
	puts $device_name
	if { [string match "*5CSE*" $device_name] } {
		set dev_name $device_name
	}
}
#set memories {}
foreach mem [get_editable_mem_instances -hardware_name $hw_name -device_name $dev_name] {
	lappend memories $mem
}
begin_memory_edit -hardware_name $hw_name -device_name $dev_name 
#write_content_to_memory -instance_index 0 -start_address 0 -word_count 1 -content "10010010"; #0x92
#write_content_to_memory -instance_index 0 -start_address 2 -word_count 1 -content "00011000"; #0x18
#write_content_to_memory -instance_index 0 -start_address 4 -word_count 1 -content "11010001"; #0xd1

#write_content_to_memory -instance_index 1 -start_address 0 -word_count 1 -content "00000000"
#write_content_to_memory -instance_index 1 -start_address 1 -word_count 1 -content "00000001"
#write_content_to_memory -instance_index 1 -start_address 2 -word_count 1 -content "00000010"
#write_content_to_memory -instance_index 1 -start_address 3 -word_count 1 -content "00000011"
#write_content_to_memory -instance_index 1 -start_address 4 -word_count 1 -content "00000100"

#write_content_to_memory -instance_index 2 -start_address 27 -word_count 1 -content "11111111"
#write_content_to_memory -instance_index 2 -start_address 28 -word_count 1 -content "10000001"
#write_content_to_memory -instance_index 2 -start_address 29 -word_count 1 -content "00011010"
#write_content_to_memory -instance_index 2 -start_address 30 -word_count 1 -content "01010111"
#write_content_to_memory -instance_index 2 -start_address 31 -word_count 1 -content "11111100"

#puts [read_content_from_memory -instance_index 0 -start_address 0 -word_count 1 -content_in_hex]
#puts [read_content_from_memory -instance_index 0 -start_address 2 -word_count 1 -content_in_hex]
#puts [read_content_from_memory -instance_index 0 -start_address 4 -word_count 1 -content_in_hex]
#save_content_from_memory_to_file -instance_index 0 -mem_file_path "C:/Users/nicho/Homework/Spring_2024/MDE/PythonShenanigans/DE1_Test_Script/test.mif" -mem_file_type mif
for { set i 0 } { $i < [llength $memories] } { incr i } {
	#set fname C:/Users/nicho/Homework/Spring_2024/MDE/PythonShenanigans/DE1_Test_Script/mem${i}.mif
	set fname RAM${i}.mif
	save_content_from_memory_to_file -instance_index $i -mem_file_path $fname -mem_file_type mif
}

end_memory_edit
