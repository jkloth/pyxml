
from xml.unicode import intl
import sys
_=intl.gettext
intl.textdomain("test1")
intl.bindtextdomain("test1",".")

capitals=(
_("Warsaw"),
_("Moscow"),
_("some more")
)
i=1
print _("The capital is %s.") % capitals[i]
