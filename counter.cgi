#!/usr/local/bin/perl
# use CGI::Carp qw(fatalsToBrowser);
use strict;
use warnings;
use CGI;
use Fcntl ':flock';

my $cgi = CGI->new;

my $count_file = "./count.dat";
my $lock_file  = "./lock.dat";   # For record IP
my $digit_len  = 6;
my $limit_time = 3600;           # 1h

# Query Analysis
my $query = $ENV{'QUERY_STRING'} || '';
my $digit = $query =~ /^(\d+)$/ ? $1 : 0;

my $ip = $ENV{'REMOTE_ADDR'} || '0.0.0.0';
my $now = time;

# ---- count up (only ?1) ----
if ($digit == 1) {

    my %iplog;

    # open IP log
    if (open(my $lf, "<", $lock_file)) {
        while (<$lf>) {
            chomp;
            my ($lip, $ltime) = split(/\t/);
            $iplog{$lip} = $ltime if $now - $ltime < $limit_time;
        }
        close $lf;
    }

    # Exclude the same IP
    unless (exists $iplog{$ip}) {

        my $fh;
        open(my $fh, "+<", $count_file) or open($fh, ">", $count_file);
        flock($fh, LOCK_EX);

        my $count = <$fh> || 0;
        $count =~ s/\D//g;
        $count++;

        seek($fh, 0, 0);
        print $fh $count;
        truncate($fh, tell($fh));
        close $fh;

        # record IP
        $iplog{$ip} = $now;
        open(my $lw, ">", $lock_file);
        flock($lw, LOCK_EX);
        for my $k (keys %iplog) {
            print $lw "$k\t$iplog{$k}\n";
        }
        close $lw;
    }
}

# ---- for display (6digit 1 ~ 6) ----
open(my $fh, "<", $count_file);
my $count = <$fh> || 0;
close $fh;

my $str = sprintf("%0*d", $digit_len, $count);
my @d = split('', $str);

$digit = 1 if $digit < 1;
$digit = $digit_len if $digit > $digit_len;

my $num = $d[$digit_len - $digit];
my $gif = "./gif/$num.gif";

print $cgi->header(-type => 'image/gif');
open(my $g, "<", $gif);
binmode $g;
binmode STDOUT;

while (read($g, my $buf, 1024)) {
    print STDOUT $buf;
}
close $g;