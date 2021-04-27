using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using API_05.Authentication;
using API_05.Models;
using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace API_05.Controllers
{
    [ApiController]
    public class IdentityController : ControllerBase
    {
        private readonly DatabaseContext _databaseContext;

        public IdentityController(DatabaseContext databaseContext)
        {
            _databaseContext = databaseContext;
        }

        [HttpPost("api/register")]
        public IActionResult RegisterUser(RegistrationModel model)
        {
            var hasher = new CustomPasswordHasher(1000);
            var identity = new Identity
            {
                Email = model.Email,
                Password = hasher.Hash(model.Password),
                FirstName = model.FirstName,
                LastName = model.LastName,
                Role = UserRole.Customer
            };
            _databaseContext.Identities.Add(identity);
            _databaseContext.SaveChanges();

            return Ok();
        }

        [HttpPost("api/login")]
        public IActionResult Token(LoginDTO loginDTO)
        {
            var identity = GetIdentity(loginDTO.Email, loginDTO.Password);
            if (identity == null)
            {
                return BadRequest(new { errorText = "Invalid username or password." });
            }

            var now = DateTime.UtcNow;
            var jwt = new JwtSecurityToken(
                    issuer: AuthOptions.ISSUER,
                    audience: AuthOptions.AUDIENCE,
                    notBefore: now,
                    claims: identity.Claims,
                    expires: now.Add(TimeSpan.FromMinutes(AuthOptions.LIFETIME)),
                    signingCredentials: new SigningCredentials(AuthOptions.GetSymmetricSecurityKey(), SecurityAlgorithms.HmacSha256));
            var encodedJwt = new JwtSecurityTokenHandler().WriteToken(jwt);

            var response = new
            {
                access_token = encodedJwt,
                username = identity.Name
            };

            return Ok(response);
        }

        private ClaimsIdentity GetIdentity(string username, string password)
        {
            var hasher = new CustomPasswordHasher(1000);

            var identity = _databaseContext.Identities.FirstOrDefault(x => x.Email == username);
            if (identity != null && hasher.Check(identity.Password, password).Verified)
            {
                var claims = new List<Claim>
                {
                    new Claim(ClaimsIdentity.DefaultNameClaimType, identity.Id.ToString()),
                    new Claim(ClaimsIdentity.DefaultRoleClaimType, identity.Role.GetString())
                };
                ClaimsIdentity claimsIdentity =
                new ClaimsIdentity(claims, "Token", ClaimsIdentity.DefaultNameClaimType,
                    ClaimsIdentity.DefaultRoleClaimType);
                return claimsIdentity;
            }

            return null;
        }
    }
}