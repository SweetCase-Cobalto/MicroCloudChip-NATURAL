=pod
    idx 0: storage root
    idx 1: app port
    idx 2: host
    idx 3: email

    idx 4: Database host
    idx 5: Database port
    idx 6: account name
    idx 7: account password
    idx 8: database name
=cut

use Cwd qw(getcwd);

# variable checking
if(@ARGV.length != 9) {
    print "argument error\n";
    exit(0);
}

# variables
my $storageRoot = $ARGV[0];
my $appPort = $ARGV[1];
my $host = $ARGV[2];
my $email = $ARGV[3];

my $databaseHost = $ARGV[4];
my $databasePort = $ARGV[5];
my $databaseUserName = $ARGV[6];
my $databaseUserPswd = $ARGV[7];
my $databaseName = $ARGV[8];

my $printFormatInBackend = "
{
    \"system\": {
        \"root\": \"$storageRoot\",
        \"port\": $appPort,
        \"host\": \"$host\"
    },
    \"database\": {
        \"rdbms\": {
            \"type\": \"mysql\",
            \"engine\": \"django.db.backends.mysql\",
            \"name\": \"$databaseName\",
            \"user\": \"$databaseUserName\",
            \"password\": \"$databaseUserPswd\",
            \"host\": \"$databaseHost\",
            \"port\": $databasePort
        }
    },
    \"admin\": {
        \"email\": \"$email\"
    }
}
";

my $hostForFrontend = "http://" . $host . ":" . $appPort;
my $printFormatInFrontend = "
{
my $printFormatInFrontend = "
{
    \"URL\": \"$hostForFrontend\"
}
";

# 디렉토리 변경
chdir "../";

# 생성할 파일 루트
my $targetBackendConfigRoot = "app/server/server/config.json";
my $targetFrontendConfigRoot = "web/src/asset/config.json";

# 파일 생성 및 재작성
if( -d $targetBackendConfigRoot ) {
    system "rm -rf $targetBackendConfigRoot";
} elsif( -e $targetBackendConfigRoot ) {
    system "rm $targetBackendConfigRoot";
}

# Config File 작성
open (FH, '>', $targetBackendConfigRoot);
print FH $printFormatInBackend;

open(FH, '>', $targetFrontendConfigRoot);
print FH $printFormatInFrontend;