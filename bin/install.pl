#!/usr/bin/perl
use JSON qw(decode_json);
use warnings;
use strict;
use feature qw( switch );
no warnings qw( experimental::smartmatch );

sub print_start_monitor { 
    # Start
    print "------------------------------\n";
    print "|                            |\n";
    print "| MicroCloudChip Installer   |\n";
    print "| App Version  0.0.1-Alpha1  |\n";
    print "| Installer Ver. 0.0.1       |\n";
    print "|                            |\n";
    print "------------------------------\n";
    print "\n\n";
}
sub print_help {
    print "MicroCloudChip Natural Installer v0.0.1\n";
    print "Usage: perl install.pl [option]\n";
    print "\n";
    print "[Option List]\n";
    print "    install - install first\n";
    print "    format - format app to first time\n";
    print "    update - update app version [not implemented]\n";
}

# Install subroutines
sub set_app_root {
    my $request_app_root
}
sub check_is_app_root_available {
    my $app_root = shift;
    
    if(-d $app_root && not -d $app_root . "/microcloudchip") {
        return 1;
    } else {
        return 0;
    }
}
sub check_is_app_port_available {
    my $app_port = shift;

    # isdigit
    my $result = $app_port =~ /^\d*$/;
    if($result == 1) {
        # is port not well known port
        $app_port = int($app_port);
        if(1024 < $app_port && $app_port < 49151) {
            return 1;
        } else {
            return 0;
        }
    } else {
        return 0;
    }
}

sub rdbms_select_process() {
    my $is_mysql = 0;
    my %mysql_config = (
        "IS_EXTERNAL" => 0,
        "ENGINE" => "django.db.backends.mysql",
        "NAME" => "",
        "USER" => "",
        "PASSWORD" => "",
        "HOST" => "",
        "PORT" => 3306
    );
    while(1) {
        printf "[3] Do You Use External Database? (Only MySQL)[y/n] (default: n to internal database) >> ";
        my $answer = "";
        chomp($answer = <STDIN>);

        if(length($answer) == 0 || $answer eq 'n') {
            printf "ok, you use internal database (SQLite)\n";
            last;
        } elsif($answer eq 'y') {
            print "you want to use external database (MySQL) lets set mysql settings.\n";
            $is_mysql = 1;
            last;
        }
    }
    
    $mysql_config{"IS_EXTERNAL"} = $is_mysql;

    # If Select externel database
    if($is_mysql) {

        my $buf = ""; # input buffer

        # Host
        while(1) {
            printf "[3-1] Host >> ";
            chomp($buf = <STDIN>);
            if(length($buf) > 0) {
                $mysql_config{"HOST"} = $buf;
                last;
            }
        }
        
        # User
        while(1) {
            printf "[3-2] Database >> ";
            chomp($buf = <STDIN>);
            if(length($buf) > 0) {
                $mysql_config{"NAME"} = $buf;
                last;
            }
        }

        # Port
        while(1) {
            printf "[3-3] Port(Default 3306) >> ";
            chomp($buf = <STDIN>);
            if(length($buf) > 0 && check_is_app_port_available($buf)) {
                $mysql_config{"PORT"} = int($buf);
                last;
            } elsif(length($buf) == 0) {
                last;
            }
        }

        # User
        while(1) {
            printf "[3-4] Username >> ";
            chomp($buf = <STDIN>);
            if(length($buf) > 0) {
                $mysql_config{"USER"} = $buf;
                last;
            }
        }

        # Password
        while(1) {
            printf "[3-5] Password >> ";
            chomp($buf = <STDIN>);
            if(length($buf) > 0) {
                $mysql_config{"PASSWORD"} = $buf;
                last;
            }
        }
    }

    return %mysql_config
}

sub process_install {
    # Variables
    # StorageRoot
    my $default_app_root = "/home/" . getpwuid($<) . "/microcloudchip"; #/home/username/microcloudchip
    my $app_root = "";

    # Port
    my $app_port = "0";
    my $default_app_port = "8000";

    while(1) {
        # Write App Root
        printf "[1] Set your app root [default: %s]>> ", $default_app_root;
        chomp($app_root = <STDIN>);

        if(length($app_root) == 0) {
            # Nothin
            printf "ok, main root will be default root: %s\n\n", $default_app_root;
            $app_root = $default_app_root;
            last;
        } else {
            if(!check_is_app_root_available($app_root)) {
                printf "This root does not exist, select other root\n";
            } else {
                # Check App Root
                $app_root = $app_root . "/microcloudchip";
                printf "Select App Root: %s\n\n", $app_root;
                last;
            }
        }
    }

    # select port
    while(1) {
        printf "[2] set your app port.[default: %s]>> ", $default_app_port;
        chomp($app_port = <STDIN>);

        if(length($app_port) == 0) {
            printf "ok, port will be default port: %s\n\n", $default_app_port;
            $app_port = $default_app_port;
            last;
        } else {
            if(!check_is_app_port_available($app_port)) {
                print "port available: 1025 ~ 49150\n";
            } else {
                printf "Port Selected %s\n\n", $app_port;
                last;
            }
        }
    }

    
    # select sql
    my %rdbms_config = rdbms_select_process();

    # Config Data를 바탕으로 데이터 처리
    my %server_config = (
        "APP_ROOT" => $app_root,
        "APP_PORT" => $app_port
    );


    # Write To Config.json
    open(FILE_CFG, ">../app/server/server/config.json");
    if($rdbms_config{"IS_EXTERNAL"}) {
    print FILE_CFG "
{
    \"system\": {
        \"storage-root\": \"$app_root\",
        \"port\": $app_port
    },
    \"database\": {
        \"rdbms\": {
            \"type\": \"mysql\",
            \"engine\": \"$rdbms_config{\"ENGINE\"}\",
            \"name\": \"$rdbms_config{\"NAME\"}\",
            \"user\": \"$rdbms_config{\"USER\"}\",
            \"password\": \"$rdbms_config{\"PASSWORD\"}\",
            \"host\": \"$rdbms_config{\"HOST\"}\",
            \"port\": $rdbms_config{\"PORT\"}
        }
    }
}
    ";
    } else {
        print FILE_CFG "
{
    \"system\": {
        \"storage-root\": \"$app_root\",
        \"port\": $app_port
    },
    \"database\": {
        \"rdbms\": {
            \"type\": \"sqlite\"
        }
    }
}
";
    }

    

    # TODO 이후 부분은 파이썬/가상환경 설치인데 차후에 코딩하자.

}
sub process_format {
    print "준비중이에오\n";
}
sub process_update {
    print "준비중이란다\n";
}

# Global Variables
my $cmd = $ARGV[0];


for ($cmd) {
    when("install") {
        print_start_monitor();
        process_install();
        last;
    } when("format") {
        print_start_monitor();
        process_format();
        last;
    } when("update") {
        print_start_monitor();
        process_update();
        last;
    } default {
        print_help();
        last;
    }
}