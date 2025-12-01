import {  ExternalLink } from "lucide-react";

const footerLinks = {
  product: [
    { name: "Features", href: "#features" },
    { name: "Download", href: "#download" },
    { name: "Demo", href: "#demo" },
  ],
  resources: [
    { name: "Documentation", href: "#" },
    { name: "Tutorials", href: "#" },
    { name: "8085 Reference", href: "#" },
  ],
  community: [
    { name: "GitHub", href: "#" },
    { name: "Report Bug", href: "#" },
    { name: "Contribute", href: "#" },
  ],
};

export const Footer = () => {
  return (
    <footer className="relative border-t border-border bg-card/50 w-full flex flex-col items-center">
      <div className="container px-4 py-8 sm:py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 sm:gap-12 mb-8 sm:mb-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-linear-to-br from-primary to-accent flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-xs sm:text-sm">
                  AS
                </span>
              </div>
              <span className="text-lg sm:text-xl font-bold">ASM Studio</span>
            </div>
            <p className="text-muted-foreground mb-4 sm:mb-6 max-w-sm text-sm sm:text-base">
              The modern IDE for 8085 assembly programming. Write, simulate, and
              debug with a beautiful notebook interface.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold mb-3 sm:mb-4 text-sm sm:text-base">Product</h4>
            <ul className="space-y-2 sm:space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-muted-foreground hover:text-primary transition-colors text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-3 sm:mb-4 text-sm sm:text-base">Resources</h4>
            <ul className="space-y-2 sm:space-y-3">
              {footerLinks.resources.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-muted-foreground hover:text-primary transition-colors text-sm inline-flex items-center gap-1"
                  >
                    {link.name}
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-3 sm:mb-4 text-sm sm:text-base">Community</h4>
            <ul className="space-y-2 sm:space-y-3">
              {footerLinks.community.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-muted-foreground hover:text-primary transition-colors text-sm"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-6 sm:pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs sm:text-sm text-muted-foreground">
            © 2024 ASM Studio. Made for learners, by learners.
          </p>
        </div>
      </div>
    </footer>
  );
};
