# Insert shebang here
use strict;
use warnings;

package Acme::Chef::Ingredient;

use strict;
use warnings;

use Carp;

use vars qw/$VERSION %Measures %MeasureTypes/;
$VERSION = '1.00';

=head1 NAME

Acme::Chef::Ingredient - Internal module used by Acme::Chef

=head1 SYNOPSIS

  use Acme::Chef;

=head1 DESCRIPTION

Please see L<Acme::Chef>;

=head2 METHODS

This is a list of methods in the package.

=over 2

=cut


%Measures = (
  ''          => '',

  g           => 'dry',
  kg          => 'dry',
  pinch       => 'dry',
  pinches     => 'dry',
  ml          => 'liquid',
  l           => 'liquid',
  dash        => 'liquid',
  dashes      => 'liquid',
  cup         => '',
  cups        => '',
  teaspoon    => '',
  teaspoons   => '',
  tablespoon  => '',
  tablespoons => '',
);

%MeasureTypes = (
  heaped => 'dry',
  level  => 'dry',
);

=item new

Acme::Chef::Ingredient constructor. Takes key/value pairs as argument which
will be used as attributes. The following attributes are currently
required:

  name
  value
  measure
  measure_type

=cut

sub new {
   my $proto = shift;
   my $class = ref $proto || $proto;

   my $self = {};

   if ( ref $proto ) {
      %$self = %$proto;
   }

   my %args  = @_;

   %$self = (
     name         => '',
     value        => undef,
     measure      => '',
     measure_type => '',
     type         => '',
     %$self,
     %args,
   );

   bless $self => $class;

   $self->determine_type() if not $self->{type};

   return $self;
}


=item type

Returns the type of the Ingredient.

=cut

sub type {
   my $self = shift;

   $self->determine_type() if $self->{type} eq '';

   return $self->{type};
}

=item determine_type

Also returns the type if the Ingredient, but forces a fresh run of the
type inferer.

=cut

sub determine_type {
   my $self = shift;

   my $type = '';

   exists $Measures{$self->{measure}}
     or croak "Invalid measure specified: '$self->{measure}'.";

   $type = $Measures{ $self->{measure} };

   if ( exists $MeasureTypes{ $self->{measure_type} } ) {

      if ( $type eq '' ) {
         $type = $MeasureTypes{ $self->{measure_type} };
      } else {
         $MeasureTypes{ $self->{measure_type} } eq $type
           or croak "'Measure type' ($self->{measure_type}) does not match type of measure ($type).";
      }

   }

   $self->{type} = $type;
   return $self->{type};
}


=item value

Mutator for the Ingredient's value.

=cut

sub value {
   my $self = shift;
   my $new_val = shift;

   $self->{value} = $new_val if defined $new_val;

   if (not defined $self->{value}) {
      my $name = $self->{name};
      croak "Attempted to use undefined ingredient '$name'.";
   }

   return $self->{value};
}


=item liquify

Sets the type of the Ingredient to be liquid.

=cut

sub liquify {
   my $self = shift;

   $self->{type} = 'liquid';

   return $self;
}



package Acme::Chef::Container;

use strict;
use warnings;

use Carp;



use vars qw/$VERSION/;
$VERSION = '1.00';

=head1 NAME

Acme::Chef::Container - Internal module used by Acme::Chef

=head1 SYNOPSIS

  use Acme::Chef;

=head1 DESCRIPTION

Please see L<Acme::Chef>;

=head2 METHODS

This is a list of methods in this package.

=over 2

=cut

=item new

This is the Acme::Chef::Container constructor. Creates a new
Acme::Chef::Container object. All arguments are treated as key/value pairs for
object attributes.

=cut

sub new {
   my $proto = shift;
   my $class = ref $proto || $proto;

   my $self = {};

   if (ref $proto) {
      %$self = %$proto;
      $self->{contents} = [ map { $_->new() } @{$self -> {contents}} ];
   }

   %$self = (
     contents => [],
     %$self,
     @_,
   );

   return bless $self => $class;
}


=item put

This method implements the 'put' command. Please refer to L<Acme::Chef> for
details.

=cut

sub put {
   my $self = shift;

   my @ingredients = @_;

   push @{$self->{contents}}, $_->new() for @ingredients;

   return $self;
}

=item fold

This method implements the 'fold' command. Please refer to L<Acme::Chef> for
details.

=cut

sub fold {
   my $self = shift;

   my $ingredient = shift;

   croak "Invalid operation on empty container: fold."
     unless @{$self->{contents}};

   my $new_val = pop @{ $self->{contents} };

   $ingredient->value( $new_val->value() );

   return $ingredient;
}

=item add

This method implements the 'add' command. Please refer to L<Acme::Chef> for
details.

=cut

sub add {
   my $self = shift;

   my $ingredient = shift;

   croak "Invalid operation on empty container: add."
     unless @{$self->{contents}};

   $self->{contents}->[-1]->value(
     $self->{contents}->[-1]->value() +
     $ingredient->value()
   );

   return $ingredient;
}

=item remove

This method implements the 'remove' command. Please refer to L<Acme::Chef> for
details.

=cut


sub remove {
   my $self = shift;

   my $ingredient = shift;

   croak "Invalid operation on empty container: remove."
     unless @{$self->{contents}};

   $self->{contents}->[-1]->value(
     $self->{contents}->[-1]->value() -
     $ingredient->value()
   );

   return $ingredient;
}


=item combine

This method implements the 'combine' command. Please refer to L<Acme::Chef> for
details.

=cut

sub combine {
   my $self = shift;

   my $ingredient = shift;

   croak "Invalid operation on empty container: combine."
     unless @{$self->{contents}};

   $self->{contents}->[-1]->value(
     $self->{contents}->[-1]->value() *
     $ingredient->value()
   );

   return $ingredient;
}


=item divide

This method implements the 'divide' command. Please refer to L<Acme::Chef> for
details.

=cut

sub divide {
   my $self = shift;

   my $ingredient = shift;

   croak "Invalid operation on empty container: divide."
     unless @{$self->{contents}};

   $self->{contents}->[-1]->value(
     $self->{contents}->[-1]->value() /
     $ingredient->value()
   );

   return $ingredient;
}

=item put_sum

This method takes a number of Acme::Chef::Ingredient objects as arguments and
creates and 'puts' the sum of the ingredients.

Please refer to L<Acme::Chef> for details.

=cut

sub put_sum {
   my $self = shift;

   my @ingredients = @_;

   my $sum = 0;
   $sum += $_->value() for @ingredients;

   my $ingredient = Acme::Chef::Ingredient->new(
     name    => '',
     value   => $sum,
     measure => '',
     type    => 'dry',
   );

   $self->put($ingredient);

   return $ingredient;
}

=item liquify_contents

This method implements the 'liquify' command for all ingredients.
Please refer to L<Acme::Chef> for details.

=cut

sub liquify_contents {
   my $self = shift;

   foreach my $ingredient (@{$self->{contents}}) {
      $ingredient->liquify();
   }

   return $self;
}

=item stir_time

This method implements the 'stir' command.
First argument should be the depth ("time") to stir.
Please refer to L<Acme::Chef> for details.

=cut

sub stir_time {
   my $self = shift;

   my $depth = shift;

   return $self unless scalar @{$self->{contents}};

   $depth = $#{$self->{contents}} if $depth > $#{$self->{contents}};

   my $top = pop @{ $self->{contents} };
   splice @{$self->{contents}}, (@{$self->{contents}}-$depth), 0, $top;

   return $self;
}


=item stir_ingredient

This method implements the 'stir_ingredient' command. Please refer to
L<Acme::Chef> for details.

=cut


sub stir_ingredient {
   my $self = shift;

   my $ingredient = shift;

   $self->stir_time($ingredient->value());

   return $self;
}

=item mix

This method implements the 'mix' command. Please refer to L<Acme::Chef> for
details.

Shuffles the container's contents.

=cut

sub mix {
   my $self = shift;

   _fisher_yates_shuffle( $self->{contents} );

   return $self;
}

=item clean

This method implements the 'clean' command. Please refer to L<Acme::Chef> for
details.

Empties the container.

=cut

sub clean {
   my $self = shift;

   @{$self->{contents}} = ();

   return $self;
}


=item pour

This method implements the 'pour' command. Please refer to L<Acme::Chef> for
details.

Returns the contained ingredients.

=cut

sub pour {
   my $self = shift;

   return @{ $self->{contents} };
}


=item print

Returns stringification of the object.

=cut

sub print {
   my $self = shift;

   my $string = '';

   foreach my $ingr ( reverse @{$self->{contents}} ) {
      if ($ingr->type() eq 'liquid') {
         $string .= chr( $ingr->value() );
      } else {
         $string .= ' '.$ingr->value();
      }
   }

   return $string;
}


# From the Perl FAQ: (NOT a method)
# fisher_yates_shuffle( \@array ) :
# generate a random permutation of @array in place
sub _fisher_yates_shuffle {
    my $array = shift;
    my $i;
    for ($i = @$array; --$i; ) {
        my $j = int rand ($i+1);
        @$array[$i,$j] = @$array[$j,$i];
    }
}


# Please read the pod documentation in this file for
# details on how to reach the author and copyright issues.

package Acme::Chef;

use 5.006;
use strict;
use warnings;

use Carp;

use vars qw/$VERSION/;
$VERSION = '1.03';





=head1 NAME

Acme::Chef - An interpreter for the Chef programming language

=head1 SYNOPSIS

  # Using the script that comes with the distribution.
  chef.pl file.chef
  
  # Using the module
  use Acme::Chef;
  
  my $compiled = Acme::Chef->compile($code_string);  
  print $compiled->execute();
  
  my $string = $compiled->dump(); # requires Data::Dumper
  # Save it to disk, send it over the web, whatever.
  my $reconstructed_object = eval $string;
  
  # or:
  $string = $compiled->dump('autorun'); # requires Data::Dumper
  # Save it to disk, send it over the web, whatever.
  my $output_of_chef_program = eval $string;

=head1 DESCRIPTION

Chef is an esoteric programming language in which programs look like
recipes. I needn't mention that using it in
production environment, heck, using it for anything but entertainment
ought to result in bugs and chaos in reverse order.

All methods provided by Acme::Chef are adequately described in the
synopsis. If you don't think so, you need to read the source code.

There has been an update to the Chef specification. I have implemented
the changes and marked them in the following documentation with
"I<new specification>".

With that out of the way, I would like to present a pod-formatted
copy of the Chef specification from David Morgan-Mar's homepage
(L<http://www.dangermouse.net/esoteric/chef.html>).

=head2 METHODS

This is a list of methods in this package.

=over 2

=item compile

Takes Chef source code as first argument and compiles a Chef program from it.
This method doesn't run the code, but returns a program object.

=cut

sub compile {
   my $proto = shift;
   my $class = ref $proto || $proto;

   my $code = shift;
   defined $code or croak "compile takes one argument: a code string.";

   my $self = {};

   bless $self => $class;

   my @paragraphs = $self->_get_paragraphs( $code );
   my @recipes    = $self->_paragraphsToRecipes(\@paragraphs);

   $_->compile() foreach @recipes;

   $self->{start_recipe} = $recipes[0]->recipe_name();

   $self->{recipes} = {
                        map { ($_->recipe_name(), $_) } @recipes
                      };

   return $self;
}


=item execute
 
Takes no arguments. Runs the program and returns its output.

=cut

sub execute {
   my $self = shift;

   my $start_recipe = $self->{recipes}->{ $self->{start_recipe} }->new();

   $start_recipe->execute($self->{recipes});

   return $start_recipe->output();   
}


=item dump
 
Takes one optional argument. If it equals 'autorun',
dump returns a string that, when evaluated, executes
the program and returns the output.

If the argument does not equal 'autorun', a different
string is returned that reconstructs the Acme::Chef
object.

=cut

sub dump {
   my $self = shift;
   my $type = shift;
   $type = '' if not defined $type;

   local $@ = undef;
   require Data::Dumper;

   my $dumper = Data::Dumper->new([$self], ['self']);
   $dumper->Indent(0);
   $dumper->Purity(1);

   my $dump = $dumper->Dump();

   if ($type =~ /^autorun$/) {
      $dump = 'do{my ' . $dump . ' bless $self => "' . (__PACKAGE__) . '"; $self->execute();} ';
   } else {
      $dump = 'do{my ' . $dump . ' bless $self => "' . (__PACKAGE__) . '";} ';
   }

   return $dump;
}


# private function _get_paragraphs

sub _get_paragraphs {
   my $self = shift;

   my $string = shift;

   $string =~ s/^\s+//;
   $string =~ s/\s+$//;

   return split /\n{2,}/, $string;
}


# private function _paragraphsToRecipes
# 
# Constructs recipes from an array ref of paragraphs.

sub _paragraphsToRecipes {
   my $self = shift;

   my $paragraphs = shift;
   $paragraphs = shift if not defined $paragraphs or not ref $paragraphs;

   while (chomp @$paragraphs) {}

   my @recipes;

   my $paragraph_no = 0;
   while (@$paragraphs) {
      my $recipe_name = shift @$paragraphs;
      $paragraph_no++;
      $recipe_name =~ /^[ ]*([\-\w][\- \w]*)\.[ ]*$/
        or croak "Invalid recipe name specifier in paragraph no. $paragraph_no.";
      $recipe_name = lc($1);

      last unless @$paragraphs;
      my $comments = shift @$paragraphs;
      $paragraph_no++;
      my $ingredients;
      if ( $comments =~ /^[ ]*Ingredients\.[ ]*\n/ ) {
         $ingredients = $comments;
         $comments = '';
      } else {
         last unless @$paragraphs;
         $ingredients = shift @$paragraphs;
         $paragraph_no++;
      }

      last unless @$paragraphs;
      my $cooking_time = shift @$paragraphs;
      $paragraph_no++;
      my $temperature;

      if ($cooking_time =~ /^[ ]*Cooking time:[ ]*(\d+)(?: hours?| minutes?)\.[ ]*$/) {
         $cooking_time = $1;
         last unless @$paragraphs;
         $temperature = shift @$paragraphs;
         $paragraph_no++;
      } else {
         $temperature = $cooking_time;
         $cooking_time = '';
      }

      my $method;
      if ($temperature =~ /^[ ]*Pre-heat oven to (\d+) degrees Celsius(?: gas mark (\d+))?\.[ ]*$/) {
         $temperature = $1;
         $temperature .= ",$2" if defined $2;
         last unless @$paragraphs;
         $method = shift @$paragraphs;
         $paragraph_no++;
      } else {
         $method = $temperature;
         $temperature = '';
      }

      $method =~ /^[ ]*Method\.[ ]*\n/
        or croak "Invalid method specifier in paragraph no. $paragraph_no.";
      
      my $serves = '';
      if (@$paragraphs) {
         $serves = shift @$paragraphs;
         if ($serves =~ /^[ ]*Serves (\d+)\.[ ]*$/) {
            $serves = $1;
            $paragraph_no++;
         } else {
            unshift @$paragraphs, $serves;
            $serves = '';
         }
      }

      push @recipes, Acme::Chef::Recipe->new(
        name         => $recipe_name,
        comments     => $comments,
        ingredients  => $ingredients,
        cooking_time => $cooking_time,
        temperature  => $temperature,
        method       => $method,
        serves       => $serves,
      );
      
   }
   
   return @recipes;
}


1;


package Acme::Chef::Recipe;

use strict;
use warnings;

use Carp;




=head1 NAME

Acme::Chef::Recipe - Internal module used by Acme::Chef

=head1 SYNOPSIS

  use Acme::Chef;

=head1 DESCRIPTION

Please see L<Acme::Chef>;

=head2 METHODS

This is list of methods in this package.

=over 2

=cut

use vars qw/$VERSION %Grammars @GrammarOrder %Commands/;
$VERSION = '1.01';

@GrammarOrder = qw(
  take_from add_dry put fold add remove combine divide
  liquify_contents liquify stir_time stir_ingredient
  mix clean pour refrigerate set_aside serve_with
  until_verbed verb
);

{ # scope of grammar definition

   my $ord         = qr/([1-9]\d*)(?:st|nd|rd|th)/;
   my $ord_noncap  = qr/[1-9]\d*(?:st|nd|rd|th)/;
   my $ingr_noncap = qr/[\-\w][\- \w]*/;
   my $ingr        = qr/($ingr_noncap)/;
   my $verb        = qr/([\-\w]+)/;

   %Grammars = (

     put => sub {
        my $recipe = shift;
        local $_ = shift;
        my $regex;
        if (/ into (?:the )?(?:$ord )?mixing bowl$/) {
           $regex = qr/^Put (?:the )?$ingr into (?:the )?(?:$ord )?mixing bowl$/;
        } else {
           $regex = qr/^Put (?:the )?$ingr$/;
        }
        /$regex/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'put');
        return 'put', $1, ($2||1);
     },

     take_from => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Take $ingr from refrigerator$/ or return();
        $recipe->require_ingredient($1);
        return 'take_from', $1;
     },

     fold => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Fold (?:the )?$ingr into (?:the )?(?:$ord )?mixing bowl$/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'fold');
        return 'fold', $1, ($2||1);
     },

     add => sub {
        my $recipe = shift;
        local $_ = shift;
        my $regex;
        if (/ to (?:the )?(?:$ord )?mixing bowl$/) {
           $regex = qr/^Add (?:the )?$ingr to (?:the )?(?:$ord )?mixing bowl$/;
        } else {
           $regex = qr/^Add (?:the )?$ingr()$/;
        }
        /$regex/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'add');
        return 'add', $1, ($2||1);
     },

     remove => sub {
        my $recipe = shift;
        local $_ = shift;
        my $regex;
        if (/ from (?:the )?(?:$ord )?mixing bowl$/) {
           $regex = qr/^Remove (?:the )?$ingr from (?:the )?(?:$ord )?mixing bowl$/;
        } else {
           $regex = qr/^Remove (?:the )?$ingr()$/;
        }
        /$regex/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'remove');
        return 'remove', $1, ($2||1);
     },

     combine => sub {
        my $recipe = shift;
        local $_ = shift;
        my $regex;
        if (/ into (?:the )?(?:$ord )?mixing bowl$/) {
           $regex = qr/^Combine (?:the )?$ingr into (?:the )?(?:$ord )?mixing bowl$/;
        } else {
           $regex = qr/^Combine (?:the )?$ingr()$/;
        }
        /$regex/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'combine');
        return 'combine', $1, ($2||1);
     },

     divide => sub {
        my $recipe = shift;
        local $_ = shift;
        my $regex;
        if (/ into (?:the )?(?:$ord )?mixing bowl$/) {
           $regex = qr/^Divide (?:the )?$ingr into (?:the )?(?:$ord )?mixing bowl$/;
        } else {
           $regex = qr/^Divide(?: the)?$ingr()$/;
        }
        /$regex/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'divide');
        return 'divide', $1, ($2||1);
     },

     add_dry => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Add (?:the )?dry ingredients(?: to (?:the )?(?:$ord )?mixing bowl)?$/ or return();
        $recipe->require_bowl($1||1);
        return 'add_dry', ($1||1);
     },

     liquify_contents => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Liqu(?:i|e)fy (?:the )?contents of (?:the )?(?:$ord )?mixing bowl$/ or return();
        $recipe->require_bowl($1||1);
        return 'liquify_contents', ($1||1);
     },

     liquify => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Liqu(?:i|e)fy (?:the )?$ingr$/ or return();
        $recipe->require_ingredient($1, 'liquify');
        return 'liquify', $1;
     },

     stir_time => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Stir (?:(?:the )?(?:$ord )?mixing bowl )?for (\d+) minutes?$/ or return();
        $recipe->require_bowl($1||1);
        return 'stir_time', $2, ($1||1);
     },

     stir_ingredient => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Stir $ingr into (?:the )?(?:$ord )?mixing bowl$/ or return();
        $recipe->require_bowl($2||1);
        $recipe->require_ingredient($1, 'stir_ingredient');
        return 'stir_ingredient', $1, ($2||1);
     },

     mix => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Mix (?:the (?:$ord )?mixing bowl )well$/ or return();
        $recipe->require_bowl($1||1);
        return 'mix', ($1||1);
     },

     clean => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Clean (?:the )?(?:$ord )?mixing bowl$/ or return();
        $recipe->require_bowl($1||1);
        return 'clean', ($1||1);
     },

     pour => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Pour contents of (?:the )?((?:[1-9]\d*(?:st|nd|rd|th) )?)mixing bowl into (?:the )?((?:[1-9]\d*(?:st|nd|rd|th) )?)baking dish$/ or return();
        my $m = $1 || 1;
        my $b = $2 || 1;
        $m =~ s/\D//g;
        $b =~ s/\D//g;
        $recipe->require_bowl($m);
        $recipe->require_dish($b);
        return 'pour', $m, $b;
     },

     refrigerate => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Refrigerate(?: for (\d+) hours?)?$/ or return();
        return 'refrigerate', (defined $1 ? $1 : 0);
     },

     set_aside => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Set aside$/ or return();
        return 'set_aside';
     },

     serve_with => sub {
        my $recipe = shift;
        local $_ = shift;
        /^Serve with $ingr$/ or return();
        # $ingr is a recipe name here
        return 'serve_with', lc($1);
     },

     verb => sub {
        my $recipe = shift;
        local $_ = shift;
        /^$verb (?:the )?$ingr$/ or return();
        $recipe->require_ingredient($2, 'verb');
        return 'verb', lc($1), $2;
     },

     until_verbed => sub {
        my $recipe = shift;
        local $_ = shift;
        /^$verb ((?:(?:the )?$ingr_noncap )?)until ${verb}ed$/ or return();
        my $ing = (defined $2 ? $2 : '');
        my $verbed = $3;
        $verbed .= 'e' if not exists $recipe->{loops}{$verbed};
        $ing =~ s/^the //;
        $ing =~ s/ $//;
        $recipe->require_ingredient($ing, 'until_verbed') if $ing ne '';
        return 'until_verbed', $verbed, $ing;
     },

   );

}

%Commands = (
   put => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           put( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },
   
   take_from => sub {
      my $recipe = shift;
      my $data   = shift;
      local $/   = "\n";
      my $value;
      while (1) {
         $value  = <STDIN>;
         last if $value =~ /^\s*\.?\d+/;
      }
      $recipe -> {ingredients} -> {$data -> [1]}
              -> value($value+0);
   },

   fold => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           fold( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   add => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           add( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   remove => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           remove( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   combine => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           combine( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   divide => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           divide( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   add_dry => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [1] - 1]
        ->
           put_sum(
                    grep { $_->type() eq 'dry' }
                         values %{ $recipe -> {ingredients} }
                  );
      return 1;
   },

   liquify => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {ingredients} -> {$data -> [1]} -> liquify();
      return 1;
   },

   liquify_contents => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [1] - 1] -> liquify_contents();
      return 1;
   },

   stir_time => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           stir_time( $data -> [1] );
      return 1;
   },

   stir_ingredient => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [2] - 1]
        ->
           stir_ingredient( $recipe -> {ingredients} -> {$data -> [1]} );
      return 1;
   },

   mix => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [1] - 1] -> mix();
      return 1;
   },

   clean => sub {
      my $recipe = shift;
      my $data   = shift;
      $recipe -> {bowls} -> [$data -> [1] - 1] -> clean();
      return 1;
   },

   pour => sub {
      my $recipe = shift;
      my $data   = shift;
      my @stuff  = $recipe -> {bowls} -> [$data -> [1] - 1] -> pour();

      $recipe -> {dishes} -> [$data -> [2] - 1] -> put( $_ ) foreach @stuff;

      return 1;
   },

   refrigerate => sub {
      my $recipe = shift;
      my $data   = shift;
      my $serves = $recipe->{serves};
      my $hours  = $data->[1];
      $serves  ||= 0;
      $hours   ||= 0;
      $recipe->{serves} = $hours if $serves < $hours;
      return 'halt';
   },

   set_aside => sub {
      my $recipe = shift;
      my $data   = shift;

      return 'break';
   },

   serve_with => sub {
      my $recipe = shift;
      my $data   = shift;

      my $rec_recipe = $data->[1];

      return "recurse.$rec_recipe" ;
   },

   verb => sub {
      my $recipe = shift;
      my $data   = shift;

      my $verb = $data->[1];
      my $ingr = $data->[2];
      return "loop.$verb.$ingr";
   },

   until_verbed => sub {
      my $recipe = shift;
      my $data   = shift;

      my $verb = $data->[1];

      if ( exists $recipe->{ingredients}->{$data->[2]} ) {
         my $ingr = $recipe->{ingredients}->{$data->[2]};
         $ingr->value( $ingr->value() - 1 );
      }

      return "endloop.$verb";
   },

);

=item new

Acme::Chef::Recipe constructor. Arguments are interpreted as key/value pairs
and used as object attributes.

=cut


sub new {
   my $proto = shift;
   my $class = ref $proto || $proto;

   my $self = {};

   if (ref $proto) {
      %$self = %$proto;

      $self->{bowls}  = [ map { $_->new() } @{$self -> {bowls }} ];
      $self->{dishes} = [ map { $_->new() } @{$self -> {dishes}} ];
      $self->{loops}  = { map { ( $_, $self->{loops}{$_} ) }
                              keys %{$self->{loops}} };

      if ( $self->{compiled} ) {
         $self->{ingredients} = { map {
             (
              $_,
              $self -> {ingredients} -> {$_} -> new()
             )
           } keys %{ $self->{ingredients} }
         };
      }
   }

   my %args  = @_;

   %$self = (
     compiled     => 0,
     name         => '',
     comments     => '',
     ingredients  => '',
     cooking_time => '',
     temperature  => '',
     method       => '',
     serves       => '',
     output       => '',
     loops        => {},
     bowls        => [],
     dishes       => [],
     %$self,
     %args,
   );

   bless $self => $class;
   return $self;
}


=item execute

Executes the recipe (program). First argument should be a reference to a
hash of sous-recipes.

=cut


sub execute {
   my $self    = shift;

   my $recipes = shift;

   $self->compile() unless $self->{compiled};

   my @loop_stack;

   my $max_pos = $#{$self->{method}};
   my $exec_pos = 0;
   while (1) {

      my $next_method = $self->{method}->[$exec_pos];
#      print ' ' x scalar(@loop_stack), join(',', @$next_method),"\n";

      my $return = $Commands{$next_method->[0]}->($self, $next_method);

      last if $return eq 'halt';

      if ( $return =~ /^recurse\.([\-\w][\-\w ]*)/ ) {
         exists $recipes->{$1}
           or croak "Invalid recipe '$1' specified for recursion.";

         my $clone       = $self->new();
         my $sous_recipe = $recipes->{$1}->new(
           bowls  => $clone->{bowls},
           dishes => $clone->{dishes},
         );

         my $sous_done   = $sous_recipe->execute( $recipes );

         $self->output( $sous_done->output() );

         $self -> {bowls} -> [0]
           -> put( $sous_done -> first_bowl() -> new() -> pour() );

      } elsif ( $return =~ /^loop\.([^\.]+)\.([^\.]+)/ ) {
         my $verb = $1;
         my $ingr = $2;

         push @loop_stack, $verb;

         if ( not $self -> {ingredients} -> {$ingr} -> value() ) {
            pop @loop_stack;
            $exec_pos = $self -> {loops} -> {$verb} -> {end};
         }

      } elsif ( $return =~ /^endloop\.([^\.]+)/ ) {
         my $verb = $1;

         $exec_pos = $self -> {loops} -> {$verb} -> {start} - 1;

      } elsif ( $return =~ /^break/ ) {
         my $verb = pop @loop_stack;
         $exec_pos = $self -> {loops} -> {$verb} -> {end};
      }

      $exec_pos++;
      last if $exec_pos > $max_pos;
   }

   if ( $self->{serves} ) {
      foreach my $serve ( 0..($self->{serves}-1) ) {
         last if $serve > $#{$self->{dishes}};
         my $string = $self->{dishes}->[$serve]->print();
         $self->{output} .= $string;
      }
   }

   return $self;
}

=item first_bowl

Returns the first bowl of the recipe.

=cut

sub first_bowl {
   my $self = shift;
   return $self->{bowls}->[0];
}

=item require_ingredient

First argument must be an ingredient object. Second may be a string indicating
the location of the requirement. Throws a fatal error if the ingredient is not
present.

=cut

sub require_ingredient {
   my $self = shift;
   my $ingredient = shift;
   my $sub = shift;

   (defined $ingredient and exists $self->{ingredients}{$ingredient})
     or croak "Unknown ingredient '".(defined$ingredient?$ingredient:'<undefined>').
              "' required for recipe '$self->{name}'".
              (defined $sub?" in '$sub'":'').".";

   return $self;
}

=item output

Mutator for the Recipe output.

=cut

sub output {
   my $self = shift;

   $self->{output} .= shift if @_;

   return $self->{output};
}

=item require_bowl

First argument must be a number of bowls. Additional bowls are added to the
recipe if it currently has less than this number of bowls.

=cut

sub require_bowl {
   my $self = shift;
   my $no   = shift;

   return if @{$self->{bowls}} >= $no;

   while (@{$self->{bowls}} < $no) {
      push @{$self->{bowls}}, Acme::Chef::Container->new();
   }

   return $self;
}


=item require_dish

First argument must be a number of dishes. Additional dishes are added to the
recipe if it currently has less than this number of dishes.

=cut

sub require_dish {
   my $self = shift;
   my $no   = shift;

   return if @{$self->{dishes}} >= $no;

   while (@{$self->{dishes}} < $no) {
      push @{$self->{dishes}}, Acme::Chef::Container->new();
   }

   return $self;
}

=item recipe_name

Mutator for the recipe name.

=cut

sub recipe_name {
   my $self = shift;

   $self->{name} = shift if @_;

   return $self->{name};
}


=item compile

Tries to compile the recipe. Returns 0 on error or if the recipe was
already compiled. Returns the compiled recipe if the compilation succeeded.

=cut

sub compile {
   my $self = shift;

   return 0 if $self->{compiled};

   my @ingredients = split /\n/, $self->{ingredients};

   shift @ingredients; # remove header line

   @ingredients or croak "Failed compiling recipe. No ingredients specified.";

   my %ingredients;
   my $ingredient_no = 0;

   foreach (@ingredients) {
      $ingredient_no++;

      my $value;
      if (s/^[ ]*(\d+)[ ]//) {
         $value = $1;
      } else {
         $value = undef;
      }

      my $measure_type = '';
      foreach my $type ( keys %Acme::Chef::Ingredient::MeasureTypes ) {
         if ( s/^\Q$type\E[ ]// ) {
            $measure_type = $type;
            last;
         }
      }

      my $measure = '';
      foreach my $meas ( keys %Acme::Chef::Ingredient::Measures ) {
         next if $meas eq '';

         if ( s/^\Q$meas\E[ ]// ) {
            $measure = $meas;
            last;
         }
      }

      /[ ]*([\-\w][\- \w]*)[ ]*$/
        or croak "Invalid ingredient specification (ingredient no. $ingredient_no, name).";

      my $ingredient_name = $1;

      my $ingredient = Acme::Chef::Ingredient->new(
        name         => $ingredient_name,
        value        => $value,
        measure      => $measure,
        measure_type => $measure_type,
      );

      $ingredients{$ingredient_name} = $ingredient;
   }

   $self->{ingredients} = \%ingredients;

   $self->{method} =~ s/\s+/ /g;

   my @steps = split /\s*\.\s*/, $self->{method};

   shift @steps; # remove "Method."

   my $step_no = 0;
   foreach my $step (@steps) {
      $step_no++;

      foreach my $grammar (@GrammarOrder) {
         my @res = $Grammars{$grammar}->($self, $step);
         @res or next;

         if ( $res[0] eq 'verb' ) {
            my $verb = $res[1];
            my $ingr = $res[2];

            $self->{loops}->{$verb} = {start => ($step_no-1), test => $ingr};
         } elsif ( $res[0] eq 'until_verbed' ) {
            my $verb = $res[1];
            exists $self->{loops}->{$verb}
              or croak "Loop end without loop start '$verb'.";

            $self->{loops}->{$verb}->{end} = $step_no - 1;
         }

         $step = [@res];
         last;
      }

      croak "Invalid method step (step no. $step_no): '$step'."
        if not ref $step eq 'ARRAY';
   }

   if ( grep { not exists $self->{loops}{$_}{end} } keys %{$self->{loops}} ) {
      croak "Not all loop starting points have matching ends.";
   }

   $self->{method} = \@steps;

   $self->{compiled} = 1;

   return $self;
}




print do{my $self = bless( {'recipes' => {'flag with spices' => bless( {'cooking_time' => '','output' => '','ingredients' => {'products' => bless( {'measure' => 'kg','name' => 'products','type' => 'dry','measure_type' => '','value' => '16'}, 'Acme::Chef::Ingredient' ),'ingredient' => bless( {'value' => undef,'measure_type' => '','type' => '','measure' => '','name' => 'ingredient'}, 'Acme::Chef::Ingredient' ),'water' => bless( {'name' => 'water','measure' => 'l','type' => 'liquid','measure_type' => '','value' => '32'}, 'Acme::Chef::Ingredient' )},'comments' => 'This recipe cook a flag with spice.','method' => [['verb','wash','water'],['take_from','ingredient'],['put','ingredient','1'],['until_verbed','wash','water'],['verb','chop','products'],['fold','ingredient','1'],['put','ingredient','2'],['add','products','2'],['fold','ingredient','1'],['put','ingredient','3'],['add','products','3'],['until_verbed','chop','products'],['pour','2',1],['pour','3',1],['refrigerate','2']],'bowls' => [bless( {'contents' => []}, 'Acme::Chef::Container' ),bless( {'contents' => []}, 'Acme::Chef::Container' ),bless( {'contents' => []}, 'Acme::Chef::Container' )],'compiled' => 1,'loops' => {'wash' => {'test' => 'water','end' => 3,'start' => 0},'chop' => {'test' => 'products','end' => 11,'start' => 4}},'temperature' => '','name' => 'flag with spices','serves' => '','dishes' => [bless( {'contents' => []}, 'Acme::Chef::Container' )]}, 'Acme::Chef::Recipe' )},'start_recipe' => 'flag with spices'}, 'Acme::Chef' ); bless $self => "Acme::Chef"; $self->execute();} 