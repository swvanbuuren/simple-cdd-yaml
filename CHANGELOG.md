# CHANGELOG

## v0.1.0 (2024-08-21)

### Chore

* chore: Move to pyproject.toml setup

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`44f5ecf`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/44f5ecff932d4a91d27459ced163361ef6367581))

### Feature

* feat: Setup automatic semantic version releases with PyPi publishing

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`9a29ee1`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/9a29ee1f6a045728a6ba885e22f275f350e38b3f))

### Fix

* fix: Correct path to version var in project configuration

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`3e8654e`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/3e8654e10261ea99d05570b37dee4cd84251be1f))

### Refactor

* refactor: Fix/document key-value parser

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`8caeb29`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/8caeb29674d1ffcee45e8f6395f38f713a9bd855))

### Unknown

* Fix repo_url in mkdocs settings

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`8ef71a9`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/8ef71a9d99f4bc6c68f122bfd8007a593b9a6ec3))

* Fix typos, formulation and links in README

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`c3f2622`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/c3f26228f20522990fbcb8daa01e85ddf7eca30d))

* Update README to mention Code Reference instead of API Reference

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`ec9badc`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/ec9badcfc1a8efb386c9302d3cb51ca872d9e60c))

* Change API Reference to Code Reference

Simple-CDD-YAML does not offer an API, therefore the naming API Reference is incorrect

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`6fd98f3`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/6fd98f3382f534fc23b1399939a8cb8f18a08aec))

* Setup documentation structure, add code reference using mkdocstrings plugin

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`65de0d0`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/65de0d074cf0694d3368fa8e3e8f0f7b28122206))

* Add link to documentation in README

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`88113ec`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/88113ec4523de0fff69fb91c2487e01bf76dd4da))

* Setup initial documentation using Material for MkDocs

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`847d216`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/847d216058559d509947bd899d9331027c1b8346))

* Update License year

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`c724401`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/c724401d44ebf772fe0d526dba88eaa336d21c33))

* Remove trailing spaces/linebreaks from Conf (env) variables

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`7cc5f09`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/7cc5f09767e6fc9ab4fb5814c66088242bdd253f))

* Overlay destination setting overrules user setting

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`c6f416e`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/c6f416e74be6772eab5b570bf347b8808707fc8b))

* Fix wrong assignment of overlay source dir

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`37197c6`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/37197c610b71198db9bbce140acd89c6f875c554))

* Handle postprocess keyword for debos correctly

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`735ea52`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/735ea52237779570286411fe781b16169f29e016))

* Add destination parameter for overlay action

Also do some refactoring

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`10a9075`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/10a9075122f4e23c268e28e602484f9a80f292d2))

* Change top-level recipe keyword &#39;recipe:&#39; to &#39;actions:&#39;

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`70e4e30`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/70e4e301d9b11cb25c8db3227095be4a6475c24c))

* Replace substitutions keyword with variables keyword

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`57cc82a`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/57cc82a2c685cc7326c757a588317d59bcb15fc7))

* Remove unnecessary print statement

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`0cb736d`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/0cb736d2578711466d05c6aaa3804dca74685331))

* Update simple-cdd-yaml cmd help message

- Include default values for chosen options
- Text consistency
- Small textual changes

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`c164081`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/c164081656d09dd290015e7a1408f174db081426))

* Add input argument to override root recipe vars

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`9521fa9`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/9521fa930a3864b04f3fa9f1cb7039e2e91ce01d))

* Remove the `dist` input argument

This is not a special input argument and there&#39;s no reason to have it as
input argument

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`d4c9012`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/d4c9012a3938a5f404b44867784eec46989e9410))

* Add Recipe done message after debos recipe finish

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`97eb921`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/97eb9212ec30f5d39eae665afc26343e07c82027))

* Add missing (second) linebreak before class def.

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`fac6203`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/fac620353d2bc0a108ecc12e472739ba340940ec))

* A few fixes to get debos recipe generation working

- Pass debos option to yaml scripts as variable
- Set $ROOTDIR correctly for overlay decompression with tar
-

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`433200a`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/433200a86b25144a40f75a18049b37df52ba1f64))

* First working version of recipe generation

Recipe still needs to be tested with debos

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`9a254d7`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/9a254d7c38c0e260ba30869e0569a86ae3341d91))

* Initial version with support only for packages

Support for other actions still needs to be added, including the special new
debos action

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`0667187`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/0667187c20c49f7845ed82016d88e9d6587e2e0a))

* Update README: include script into run action

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`b380093`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/b38009384553c5799f198a6b5ffc8b3d32fa5de5))

* Combine run and script action into one action

Use the same action syntax as debos. Whether script or command is chosen
is defined by the presence of the script or command keyword.

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`dc82f1f`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/dc82f1f2bacd42b1fdf7fe61783d04f2c1618221))

* Remove useless return None statements

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`0f5ee02`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/0f5ee020a628ab63341160890a3d6bb88dc20f6d))

* Remove unnecessary action debug print statements

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`f7ba86e`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/f7ba86e224e872297c4c6727865576609310fe16))

* Fix ModuleNotFoundError

Repalce find_namespace_packages with tradional find_packages call

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`1d3f8d8`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/1d3f8d8efafc0e4845a3cb8ee59bab0f94092df1))

* Add introduction to README

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`44b4744`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/44b4744b11221d01c7beb4f504d921ff3bcb14f1))

* Add comments, rename variable in actions

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`7ced34b`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/7ced34b3d2d8182ffc22e72ba27fe9f72f81790f))

* Linebreaks and Examples section in README

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`93c8fb0`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/93c8fb0a498256498afc2ab64383b6065e24bde2))

* Update README

- Change name eeverywhere to Simple-CDD-YAML
- Fix license reference

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`f9e05d6`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/f9e05d6a443e1914356e8a0c42ac4b66189c9496))

* Allow recipe from other directory (git submodule)

- Add working_dir keyword for recipe action
- Action now requires a dict with input arguments
- Include recipes from other directory with own scripts and overlays
- E.g. from a git submodule from upstream

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`179b9b8`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/179b9b80e37edc0eb336a83d53224dbacef6c533))

* Remove unnecessary line break in run action

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`4492d2d`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/4492d2d5ece7539503555bb918e61ad9da694f9d))

* Add working_dir option to recipe action

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`b7ce0e3`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/b7ce0e33e78430edc0313c32df1b110832598fae))

* Add user option to run action

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`a7ccb12`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/a7ccb127cde84fa24f6bef5b3703953b291684b3))

* Newline after initial postinst part for increased readability

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`ebcb865`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/ebcb86572905222e89740e6b2ecb03a6b2a88a01))

* Set args profile from recipe in dedicated method

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`1a79d47`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/1a79d47dcf6475eefb4b52652607fde21fc55b56))

* Try to resolve profile name from recipe

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`2d643b9`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/2d643b9a6d9d4ba02e2d325a9fde52e3d28a489c))

* Move example recipes to simple-cdd-yaml-recipes

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`a230f22`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/a230f224dc758ad7993ba84083eb4247896bc08a))

* Add link to Simple-CDD in README

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`3f3276c`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/3f3276c0a981400186587281a8e98eb16129a65a))

* Set correct owner  for overlay rollout

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`9a58d3e`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/9a58d3eba0946a27e1b7a6a9a32e51cdb538e682))

* Fix bugs and recipes

- fix in postint
- fix extra action output
- added .gitignore

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`f56cfaf`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/f56cfaf3e47299f5994b038c1848e2c4d286293e))

* Initial commit

Signed-off-by: Sietze van Buuren &lt;s.van.buuren@gmail.com&gt; ([`bf210e0`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/bf210e06111514de2bb2a20591e30c4074318bb6))

* Initial commit ([`eab5e54`](https://github.com/swvanbuuren/simple-cdd-yaml/commit/eab5e544a0683117a3cee33c895ace202a7dd98f))
