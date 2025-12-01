import { Creator } from "../components/Creator";
import { DemoPreview } from "../components/DemoPreview";
import { Downloads } from "../components/Downloads";
import { Features } from "../components/Features";
import { Footer } from "../components/Footer";
import { Hero } from "../components/Hero";
import { Navbar } from "../components/Navbar";

const Home = () => {
  return (
    <div className="min-h-screen w-full">
      <Navbar />
      <Hero />
      <section className="flex flex-col w-full items-center">
        <Features />
        <DemoPreview />
        <Creator />
        <Downloads />
      </section>
      <Footer />
    </div>
  );
};

export default Home;
