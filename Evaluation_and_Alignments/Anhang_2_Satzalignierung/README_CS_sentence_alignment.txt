Sentence alignment Credit Suisse (CS) Bulletins
Scripts: Fabienne Leuenberger 
Based on: Text+Berg scripts (Johannes Graen, Manuela Weibel, Fabienne Leuenberger)
Documentation: Fabienne Leuenberger
June 2015
*****************************************************
Remark: use Unix screen if working on CL server
*****************************************************
Step 1: Preparation of the data to be aligned

a)	Create new directory
		$ mkdir sentence_alignment

b)	Put the parallel data of CS (or entire release) inside directory created in a), in a directory called 
	“CS_bulletins”

c)	Put the alignment XML file “Aligned_xml_files.xml” inside directory created in a)

d)	Put the following 3 Python scripts inside directory “sentence_alignment”:
		- cs_extractfactoredparallelcorpus.py
		- cs_extract_sentence_alignment_information_BLEUalign.py
		- cs_overview_aligned_sentences.py

e)	Copy the directory “Bleualign” into your directory “sentence_alignment”
	Location in kitt server: /home/clbergtext/Sentence_Alignment/Bleualign/

f)	Use the Python script “cs_extractfactoredparallelcorpus.py”
	It uses the alignment information to extract the aligned data all in one file per language. 
	Format: 1 XML sentence per line, token|bookID_bookLang-articleID-sentID-WordID
	Output: files “L1.out” and “L2.out”
		
		$ python cs_extractfactoredparallelcorpus.py L1-L2
			-> L1-L2 must be de-fr, de-it, de-en, fr-it, en-fr, it-en

g)	Important remark: the script does not accept multiple article alignments. If there are multiple article 
	alignment in file “Aligned_xml_files.xml”, then only the first article alignment will be taken for the 
	sentence alignment extraction.

h)	Be aware, the output files of e) might contain empty lines which must be removed. Else, errors might appear 
	in the sentence alignment.
		$ sed -i '/^$/d' L1.out 	(ex: $ sed -i '/^$/d' fr.out)
		$ sed -i '/^$/d' L2.out	(ex: $ sed -i '/^$/d' it.out)

*****************************************************
Step 2: Translate L1 output data into L2 (Unix screen!)

a)	Create directory “SMT” inside directory “sentence_alignment”
		$ mkdir SMT

b)	Put the SMT system directory you need inside directory “SMT”
		de-fr
		de-it
		de-en
		fr-it
		en-fr
		it-en

	$ cp -r /mnt/storage/hal2/users/leuenberger/cs_alignment/SMT/de-en  sentence_alignment/SMT 

	—> these directories contain (1) “moses.ini” file, (2) phrase table, (3) language model and (4) a 
	   lowercasing Perl script

c)	Change the two paths inside “moses.ini” file as indicated in the file, into the path where “moses.ini” is 
	located (de-fr: 3 paths to change!) —> pwd of “moses.ini” directory


d)	Translation with Moses using the SMT system of a) (pwd: “/home/user/…/sentence_alignment”)

		For sentence alignment DE-FR:
			$ cat de-fr/de.out|SMT/de-fr/lowercase.perl|moses -f SMT/de-fr/moses.ini|sed -r "s/^\.eoa/.EOA/" > de-fr/de_fr.trans

		For sentence alignment DE-IT
			$ cat de-it/de.out|SMT/de-it/lowercase.perl|moses -f SMT/de-it/moses.ini|sed -r "s/^\.eoa/.EOA/" > de-it/de_it.trans

		For sentence alignment DE-EN
			$ cat de-en/de.out|SMT/de-en/lowercase.perl|moses -f SMT/de-en/moses.ini|sed -r "s/^\.eoa/.EOA/" > de-en/de_en.trans

		For sentence alignment FR-IT
			$ cat fr-it/fr.out|SMT/fr-it/lowercase.perl|moses -f SMT/fr-it/moses.ini|sed -r "s/^\.eoa/.EOA/" > fr-it/fr_it.trans

		For sentence alignment EN-FR
			$ cat en-fr/en.out|SMT/en-fr/lowercase.perl|moses -f SMT/en-fr/moses.ini|sed -r "s/^\.eoa/.EOA/" > en-fr/en_fr.trans

		For sentence alignment IT-EN
			$ cat it-en/it.out|SMT/it-en/lowercase.perl|moses -f SMT/it-en/moses.ini|sed -r "s/^\.eoa/.EOA/" > it-en/it_en.trans

*****************************************************
Step 3: Use Bleualign to sentence align the translation of step 2 with the output data in L2 of step 1

a)	Put the script “bleualign.py” inside the directory “sentence_alignment”

b)	Use the script “bleualign.py”
		$ Bleualign/bleualign.py -s L1-L2/L1.out -t L1-L2/L2.out —-srctotarget L1-L2/L1_L2.trans -o L1-L2/L1_L2.align2 —-factored -v 3

	For sentence alignment DE-FR:
		$ Bleualign/bleualign.py -s de-fr/de.out -t de-fr/fr.out --srctotarget de-fr/de_fr.trans -o de-fr/de_fr.align2 --factored -v 3


	For sentence alignment DE-IT:
		$ Bleualign/bleualign.py -s de-it/de.out -t de-it/it.out --srctotarget de-it/de_it.trans -o de-it/de_it.align2 --factored -v 3


	For sentence alignment DE-EN:
		$ Bleualign/bleualign.py -s de-en/de.out -t de-en/en.out —-srctotarget de-en/de_en.trans -o de-en/de_en.align2 —-factored -v 3

	For sentence alignment FR-IT:
		$ Bleualign/bleualign.py -s fr-it/fr.out -t fr-it/it.out --srctotarget fr-it/fr_it.trans -o fr-it/fr_it.align2 --factored -v 3
	
	For sentence alignment EN-FR:
		$ Bleualign/bleualign.py -s en-fr/en.out -t en-fr/fr.out —-srctotarget en-fr/en_fr.trans -o en-fr/en_fr.align2 —-factored -v 3

	For sentence alignment IT-EN:
		$ Bleualign/bleualign.py -s it-en/it.out -t it-en/en.out -—srctotarget it-en/it_en.trans -o it-en/it_en.align2 —-factored -v 3

c)	Results: one file in L1 and one file in L2 where aligned sentences are on the same line
		L1_L2.align2-s (source) and L1_L2.align2-t (target)

d)	You can have a look at how the two data are aligned with the command:
		$ paste L1_L2.align2-* | more

*****************************************************
Step 4: Transformation of Bleualign output format into XML sentence alignment format

a)	Use the Python script “cs_extract_sentence_alignment_information_BLEUalign.py”
		$ python cs_extract_sentence_alignment_information_BLEUalign.py [L1-L2/L1_L2.align2-s] [L1-L2/L1_L2.align2-t]

	For sentence alignment DE-FR:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py de-fr/de_fr.align2-s de-fr/de_fr.align2-t

	For sentence alignment DE-IT:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py de-it/de_it.align2-s de-it/de_it.align2-t

	For sentence alignment DE-EN:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py de-en/de_en.align2-s de-en/de_en.align2-t

	For sentence alignment FR-IT:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py fr-it/fr_it.align2-s fr-it/fr_it.align2-s

	For sentence alignment EN-FR:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py en-fr/en_fr.align2-s en-fr/en_fr.align2-t

	For sentence alignment IT-EN:
		$ python cs_extract_sentence_alignment_information_BLEUalign.py it-en/it_en.align2-s it-en/it_en.align2-t

b)	Results: the script creates a directory “S-Align_Files_L1-L2” where for each XML parallel data, a XML file 
	containing the aligned sentences in TEI XML is created. In addition, information about the type of the 
	sentence alignment is also provided.

c)	Use the script “cs_overview_aligned_sentences.py” if you want to get an overview of the sentence alignment
		$ python cs_overview_aligned_sentences.py L1-L2
			-> L1-L2 must be de-fr, de-it, de-en, fr-it, en-fr, it-en

d)	You can now export the sentence alignment directory “S-Align_Files_L1-L2” to your computer.

