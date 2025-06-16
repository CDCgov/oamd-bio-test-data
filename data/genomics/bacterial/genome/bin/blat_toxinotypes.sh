#!/bin/bash -l

#$ -o 	blattox.out
#$ -e 	blattox.err
#$ -N 	blattox
#$ -cwd
#$ -q short.q

#
# Description: Quick and dirty way to run blat with dnaX mode AND to sort and trim the output psl files
#
# Usage: ./blat_toxinotypes.sh -i input_assembly -o output_file -d AA_database_to_compare_to -t toxinotype_def_file
#
# Output location: Varies on contents
#
# Modules required: blat
#
# v1.0 (09/08/2020)
#
# Created by Nick Vlachos (nvx4@cdc.gov)
#

#  Function to print out help blurb
show_help () {
	echo "Usage is ./blat_toxinotypes.sh -i input_assembly -o output_file -d AA_database_to_compare_to -t toxinotype_def_file"
}

version=1.0

# Parse command line options
options_found=0
while getopts ":h?i:o:d:t:p:V" option; do
	options_found=$(( options_found + 1 ))
	case "${option}" in
		\?)
			echo "Invalid option found: ${OPTARG}"
      show_help
      exit 0
      ;;
		i)
			echo "Option -i triggered, argument = ${OPTARG}"
			input=${OPTARG};;
		o)
			echo "Option -o triggered, argument = ${OPTARG}"
			sample_name=${OPTARG};;
		d)
			echo "Option -d triggered, argument = ${OPTARG}"
			DB=${OPTARG};;
		t)
			echo "Option -f triggered, argument = ${OPTARG}"
			tox_def_file=${OPTARG};;
		p)
			echo "Option -p triggered"
			terra=${OPTARG};;
		V)
			show_version="True";;
		:)
			echo "Option -${OPTARG} requires as argument";;
		h)
			show_help
			exit 0
			;;
	esac
done

if [[ "${show_version}" = "True" ]]; then
	echo "${version}"
	exit
fi

# Show help info for when no options are given
if [[ "${options_found}" -eq 0 ]]; then
	echo "No options found"
	show_help
	exit
fi

# Checks for proper argumentation
 if [[ ! -f "${input}" ]] || [[ -z "${input}" ]]; then
 	echo "Assembly empty or non-existent, exiting"
 	exit 1
 fi

# Checks for proper argumentation
 if [[ ! -f "${DB}" ]] || [[ -z "${DB}" ]]; then
 	echo "Database empty or non-existent, exiting"
 	exit 1
fi

# set the correct path for blat - needed for terra
if [[ $terra = "terra" ]]; then
	blat_path=/opt/conda/envs/phoenix/bin/
else
	blat_path=""
fi

db_name=$(basename ${DB} .fa)
${blat_path}blat -q=prot -t=dnax ${input} ${DB} -minIdentity=100 -noHead ${sample_name}_${db_name}.psl


header="ID\tToxinotype\tToxin\tsub-type\tContig\tStart\tStop"

ToxA_default="${sample_name}\tToxin-A\tN/A\tN/A\tN/A\tN/A\n"
ToxB_default="${sample_name}\tToxin-B\tN/A\tN/A\tN/A\tN/A\n"

A_found="False"
B_found="False"
A_count=0
B_count=0

# Loop through and act on each sample name in the passed/provided list
while IFS= read -r var; do
    type="unset"
    sub_type="unset"
    contig_start="unset"
    contig_stop="unset"
    toxinotype="Unknown"
	IFS='	' read -r -a line_array <<< "$var"
	echo ${line_array[@]}
    matches=${line_array[0]}
    total_length=${line_array[10]}
    echo "M=${matches}:TL-${total_length}"
    if [[ ${matches} -eq ${total_length} ]]; then
        sub_type=${line_array[9]}
        contig=${line_array[13]}
        contig_start=${line_array[15]}
        contig_stop=${line_array[16]}
        first_sub_type=${sub_type:0:1}
        if [[ "${first_sub_type^}" = "A" ]]; then
            type="Toxin-A"
            A_found="True"
            A_count=$(( A_count + 1))
            A_sub_type=${line_array[9]}
        elif [[ "${first_sub_type^}" = "B" ]]; then
            type="Toxin-B"
            B_found="True"
            B_count=$(( B_count + 1))
            B_sub_type=${line_array[9]}
        elif [[ "${first_sub_type^}" = "S" ]]; then
            if [[ "${sub_type}" = *"sordellii_group"* ]] || [[ "${sub_type}" = *"sordellii_TcsL"* ]]; then
                type="Toxin-B"
                B_found="True"
                B_count=$(( B_count + 1))
                B_sub_type=${line_array[9]}
            elif [[ "${sub_type}" = *"sordelii_TcsH"* ]]; then
                type="Toxin-A"
                A_found="True"
                A_count=$(( A_count + 1))
                A_sub_type=${line_array[9]}
            fi
        fi
        echo -e "${sample_name}\t${type}\t${sub_type}\t${contig}\t${contig_start}\t${contig_stop}" >> ${sample_name}_${db_name}.tmx
    fi
done < "${sample_name}_${db_name}.psl"

#echo -e "AF:${A_found}\nAD:${ToxA_default}\nBF:${B_found}\nBD:${ToxB_default}"

if [[ "${A_found}" = "False" ]]; then
    echo -e "${ToxA_default}" >> ${sample_name}_${db_name}.tmx
fi
if [[ "${B_found}" = "False" ]]; then
    echo -e "${ToxB_default}" >> ${sample_name}_${db_name}.tmx
fi
total_toxs_count=$(( A_count + B_count))
echo "Count check ${A_count},${B_count},${total_toxs_count}"
if [[ "${total_toxs_count}" -eq 0 ]]; then
    toxinotype="No subtypes found"
elif [[ "${total_toxs_count}" -eq 1 ]] || [[ "${total_toxs_count}" -eq 2 ]]; then
    # Look up toxinotype
    if [[ "${A_sub_type}" = "unset" ]] || [[ "${A_sub_type}" = "" ]] || [[ -z ${A_sub_type} ]]; then
        tmp_A_subtype="-"
    else
        tmp_A_subtype="${A_sub_type}"
    fi
    if [[ "${B-sub_type}" = "unset" ]] || [[ "${B-sub_type}" = "" ]]; then
        tmp_B_subtype="-"
    else
        tmp_B_subtype="${B_sub_type}"
    fi
    while IFS= read -r var2; do
        IFS='	' read -r -a line_array2 <<< "$var2"
        echo -e "${line_array2[@]}"
        file_subA=${line_array2[4]}
        file_subB=${line_array2[5]}
        file_ttype=${line_array2[0]}
        echo -e "|${tmp_A_subtype}| = |${file_subA}| : |${tmp_B_subtype}| = |${file_subB}|"
        if [[ "${tmp_A_subtype}" = "${file_subA}" ]] && [[ "${tmp_B_subtype}" = "${file_subB}" ]]; then
            toxinotype="${file_ttype}"
            break
        fi
    done < "${tox_def_file}"
    if [[ "${toxinotype}" = "Unknown" ]]; then
        toxinotype="Undefined"
    fi
else
    toxinotype="Too_many_subtypes"
fi


sort -k2 ${sample_name}_${db_name}.tmx > ${sample_name}_${db_name}.tsx

echo -e "${header}" > ${sample_name}_${db_name}.tmp
cat ${sample_name}_${db_name}.tmp ${sample_name}_${db_name}.tsx > ${sample_name}_${db_name}.tox
echo -e "Toxinotype:\t${toxinotype}" >> ${sample_name}_${db_name}.tox

rm ${sample_name}_${db_name}.tmx ${sample_name}_${db_name}.tmp

# Send a completion email to whoever ran the script
echo "All isolates completed"
global_end_time=$(date "+%m-%d-%Y @ %Hh_%Mm_%Ss")
#Script exited gracefully (unless something else inside failed)
#printf "%s %s" "Act_by_list_template.sh has completed check of snd MLSTs" "${global_end_time}" | mail -s "act_by_list complete" nvx4@cdc.gov
exit 0
