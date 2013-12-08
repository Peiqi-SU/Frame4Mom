#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use POSIX qw(strftime);

$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $dir_path = dirname(__FILE__);
my $upload_dir = "$dir_path/upload";

my $query = new CGI;
my $filename = $query->param("yourname");
my $filedescription = $query->param("description");
my $id = $query->param("id");

print $query->header ( );
#print $filename;
if ( !$filename ){
    print "There was a problem uploading your photo, please make sure to upload a photo.";
    exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ ){
    $filename = $1;
}else{
    die "Filename contains invalid characters";
}

my $upload_filehandle = $query->upload("yourname");

my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time());
my $format_time=sprintf("%d-%d-%d~%d_%d_%d",$year+1990,$mon+1,$mday,$hour,$min,$sec);
$filename = $format_time . ".jpg";

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle>){
    print UPLOADFILE;
}

close UPLOADFILE;


open (MYFILE, ">$dir_path/newestfile.txt");
print MYFILE $filename;
close (MYFILE); 

open (MYFILE, ">$dir_path/newestfileDescription.txt");
print MYFILE $filedescription;
close (MYFILE); 

print "<html><head><script language=\"javascript\" type=\"text/javascript\">window.location.href=\"http://192.168.11.8/~peiqisu/Frame4Mom/uploaded.html\"</script></head><body></body></html>"
