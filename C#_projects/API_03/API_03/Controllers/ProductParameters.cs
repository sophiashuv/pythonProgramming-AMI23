using System;
namespace API_03.Controllers
{
	public class ProductParameters
	{
		public int PageNumber { get; set; } = 1;
		public int Offset {get; set;}
		public int PageSize { get; set; }
		public string Sort_by { get; set; } = "_title";
		public string Sort_type { get; set; } = "asc";
		public string Search { get; set; }
	}
}

