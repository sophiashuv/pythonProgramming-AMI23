using System;
using System.Globalization;
using System.Linq;

namespace API_03.Models
{
    public static class Validation
    {

        public static string ValidateTitle(string value)
        {
            try
            {
                if (value == "0") return value;
                if (value.Any(char.IsDigit))
                {
                    throw new ArgumentException("Title must not contain integers.");
                }
                return value;
            }
            catch (Exception)
            {
                return null;
            }
        }

        public static double ValidatePrice(double value)
        {
            try
            {
                value = Math.Round(value, 2);

                string strValue = value.ToString(CultureInfo.InvariantCulture).
                    IndexOf(".", StringComparison.Ordinal) == -1 ? value.ToString(CultureInfo.InvariantCulture)
                                                                   + "." : value.ToString(CultureInfo.InvariantCulture);
                if (strValue.Substring(strValue.IndexOf(".", StringComparison.Ordinal)).Length > 3)
                {
                    throw new ArgumentException("Price must have two digits after coma.");
                }

                return value;
            }
            catch (Exception)
            {
                return 0;
            }
}

        public static string ValidateDate(string value)
        {
            try { 
                if (value == "0") return value;
                DateTime v = DateTime.Parse(value);
                if (DateTime.Compare(DateTime.Now, v) < 0)
                {
                    throw new ArgumentException("Non-existent Date.");
                }
                return v.ToString("yyyy-MM-dd");
            }
            catch (Exception)
            {
                return null;
            }
        }

        public static string ValidateDate(string value1, string value2)
        {
            try
            {
                if (value2 == "0") return value2;
                DateTime v1 = DateTime.Parse(value1);
                DateTime v2 = DateTime.Parse(value2);
                if (DateTime.Compare(v1, v2) > 0)
                {
                    throw new ArgumentException("Incorrect data, created_at must be lover than updated_at.");
                }
                return ValidateDate(value2);
            }
            catch (Exception)
            {
                return null;
            }
        }

        public static string ValidateImage_url(string value)
        {
            try { 
                if (value == "0") return value;
                string[] validImageExtensions = { ".jpg", ".jpeg", ".png", ".gif" };
                if (!validImageExtensions.Any(value.EndsWith))
                {
                    throw new ArgumentException("Incorrect image_url.");
                }
                return value;
            }
            catch (Exception)
            {
                return null;
            }
        }    
    }
}
