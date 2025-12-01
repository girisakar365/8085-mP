import { motion } from "framer-motion";
import { Heart } from "lucide-react";

export const Creator = () => {
  return (
    <section
      id="about"
      className="relative py-12 sm:py-16 md:py-20 lg:py-28 overflow-hidden w-full flex flex-col items-center"
    >
      {/* Background */}
      <div className="absolute inset-0 bg-linear-to-b from-background via-secondary/10 to-background" />

      <div className="container relative z-10 px-4 sm:px-6 md:px-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-10 sm:mb-12 md:mb-16"
        >
          <span className="text-primary font-semibold text-xs sm:text-sm tracking-wider uppercase mb-3 sm:mb-4 block">
            About
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold">
            Meet the <span className="gradient-text">Creator</span>
          </h2>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto"
        >
          <div className="glass-card p-6 sm:p-8 md:p-12 text-center relative overflow-hidden rounded-2xl ">
            {/* Decorative gradient */}
            <div className="absolute top-0 right-0 w-40 sm:w-52 md:w-64 h-40 sm:h-52 md:h-64 bg-linear-to-bl from-primary/20 to-transparent rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-32 sm:w-40 md:w-48 h-32 sm:h-40 md:h-48 bg-linear-to-tr from-accent/20 to-transparent rounded-full blur-3xl" />

            <div className="relative z-10">
              {/* Avatar Section */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-10 sm:gap-16 mb-8">
                {/* Creator 1 */}
                <div>
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    whileInView={{ scale: 1, opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 }}
                    className="w-28 h-28 sm:w-32 sm:h-32 mx-auto mb-4 relative cursor-pointer"
                  >
                    <a href="#" target="_blank" rel="noopener noreferrer">
                      <div className="absolute inset-0 bg-linear-to-br from-primary to-accent rounded-full animate-pulse-glow" />
                      <div className="absolute inset-1 bg-card rounded-full flex items-center justify-center">
                        <span className="text-3xl sm:text-4xl font-bold gradient-text">AS1</span>
                      </div>
                    </a>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 }}
                  >
                    <h3 className="text-xl sm:text-2xl font-bold mb-1">Developer Name</h3>
                  </motion.div>
                </div>

                {/* Creator 2 */}
                <div>
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    whileInView={{ scale: 1, opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 }}
                    className="w-28 h-28 sm:w-32 sm:h-32 mx-auto mb-4 relative cursor-pointer"
                  >
                    <a href="#" target="_blank" rel="noopener noreferrer">
                      <div className="absolute inset-0 bg-linear-to-br from-primary to-accent rounded-full animate-pulse-glow" />
                      <div className="absolute inset-1 bg-card rounded-full flex items-center justify-center">
                        <span className="text-3xl sm:text-4xl font-bold gradient-text">AS2</span>
                      </div>
                    </a>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 }}
                  >
                    <h3 className="text-xl sm:text-2xl font-bold mb-1">Developer Name</h3>
                  </motion.div>
                </div>
              </div>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.4 }}
                className="text-muted-foreground mb-6 sm:mb-8 max-w-md mx-auto text-sm sm:text-base leading-relaxed"
              >
                Passionate about retro computing, education, and developer tools. Building ASM Studio to make learning 8085 assembly programming modern and enjoyable.
              </motion.p>

              <motion.div
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.6 }}
                className="flex items-center justify-center gap-2 text-muted-foreground text-sm"
              >
                <span>Built with</span>
                <Heart className="w-4 h-4 text-destructive fill-destructive" />
                <span>for the 8085 community</span>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};