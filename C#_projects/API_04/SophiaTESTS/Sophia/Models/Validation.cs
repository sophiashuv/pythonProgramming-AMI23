using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Linq;
using System.Threading.Tasks;

namespace Sophia.Models
{
    public static class Validation
    {
        public class TitleAttribute : ValidationAttribute
        {
            public override bool IsValid(object value)
            {
                string strValue = value as string;
                if (strValue.Any(char.IsDigit))
                {
                    ErrorMessage = "Title must not contain integers.";
                    return false;
                }
                return true;
            }
        }


        public class ImageUrlAttribute : ValidationAttribute
        {
            public override bool IsValid(object value)
            {
                string strValue = value as string;
                string[] validImageExtensions = { ".jpg", ".jpeg", ".png", ".gif" };
                if (!validImageExtensions.Any(strValue.EndsWith))
                {
                    ErrorMessage = "Incorrect image_url.";
                    return false;
                }
                return true;
            }
        }


        public class PriceAttribute : ValidationAttribute
        {
            public override bool IsValid(object value)
            {
                double dValue = ((IConvertible)value).ToDouble(null);
                string strValue = dValue.ToString(CultureInfo.InvariantCulture).
               IndexOf(".", StringComparison.Ordinal) == -1 ? dValue.ToString(CultureInfo.InvariantCulture)
                                                              + "." : dValue.ToString(CultureInfo.InvariantCulture);

                if (strValue.Substring(strValue.IndexOf(".", StringComparison.Ordinal)).Length > 3)
                {
                    ErrorMessage = "Price must have two digits after coma.";
                    return false;
                }
                return true;
            }
        }


        public class DateAttribute : ValidationAttribute
        {
            public override bool IsValid(object value)
            {
                string strValue = value as string;
                try
                {
                    DateTime v = DateTime.Parse(strValue);
                    if (DateTime.Compare(DateTime.Now, v) < 0)
                    {
                        ErrorMessage = "Non-existent Date.";
                        return false;
                    }
                    return true;
                }
                catch (Exception e)
                {
                    ErrorMessage = e.Message;
                    return false;
                }
            }
        }
    }
}