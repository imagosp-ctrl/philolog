# Philolog AI Agents

## Project Overview
Philolog is an interactive Koine Greek learning platform focused on Orthodox liturgical texts. This document outlines the AI agents and automated systems that support the project.

## Current Agents

### 1. GitHub Copilot
**Role**: Primary coding assistant and development support
**Capabilities**:
- Code completion and generation
- Bug fixing and debugging
- File structure management
- Feature implementation
- Documentation assistance

**Recent Contributions**:
- Updated project title from "Koine Greek Study Center" to "Philolog"
- Fixed JSON file formatting issues
- Created project folder structure
- Assisted with HTML/CSS/JavaScript development

#### GitHub Copilot Workflows for Philolog

**Text Processing Pipeline**:
- JSON structure validation for Greek liturgical texts
- Vue.js component development for interactive learning
- CSS styling for Orthodox-themed UI design
- Drag-and-drop functionality for text reconstruction games

**Liturgical Content Assistance**:
- Greek text encoding and Unicode handling
- Phonetic transcription formatting
- Grammar color-coding implementation
- Interactive tooltip systems
- Professional typography implementation with Google Fonts integration
- Hero image optimization and overlay design

## Philolog UI Build Structure

### Standard Page Architecture
All Philolog pages follow this exact structural pattern to maintain visual consistency:

#### HTML Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>[Page Name] — Philolog</title>
  <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Montserrat:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* [Page-specific styles here] */
  </style>
</head>
<body>
  <!-- Standard Header -->
  <nav class="top-nav">
    <div class="nav-container">
      <a href="/" class="nav-logo">
        <div class="logo-icon">Φ</div>
        <span>Philolog</span>
      </a>
      <ul class="nav-links" style="display:flex;gap:1rem;list-style:none">
        <li><a href="index.html" style="text-decoration:none;color:inherit">Home</a></li>
      </ul>
    </div>
  </nav>

  <!-- Hero Section with Card -->
  <section class="framed-section" style="margin-top:64px">
    <div class="framed-card">
      <div class="framed-card__content">
        <!-- Page-specific content here -->
      </div>
    </div>
  </section>

  <script>
    /* Page-specific JavaScript */
  </script>
</body>
</html>
```

#### Required CSS Base Classes
```css
/* Minimal base and header styles - REQUIRED FOR ALL PAGES */
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Montserrat','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;color:#1f2937;background:#fff;line-height:1.6}
.top-nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(255,255,255,0.95);backdrop-filter:blur(10px);border-bottom:1px solid rgba(0,0,0,0.08);padding:0 2rem;height:64px}
.nav-container{max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:100%}
.nav-logo{display:flex;align-items:center;gap:.5rem;font-weight:600;text-decoration:none;color:inherit;font-family:'Lora',serif}
.logo-icon{width:32px;height:32px;background:#3b82f6;border-radius:6px;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold}

/* Framed section styles - REQUIRED FOR HERO IMPLEMENTATION */
.framed-section{position:relative;padding:80px 0;overflow:visible}
.framed-section::before{content:'';position:absolute;inset:0;background-image:url('./public/images/[PAGE_HERO_IMAGE].jpg');background-size:cover;background-position:center;opacity:.8;filter:brightness(.85);z-index:0}
.framed-section .framed-card{position:relative;z-index:1;max-width:1140px;margin:0 auto;background:rgba(255,255,255,0.90);border-radius:30px;box-shadow:0 10px 30px rgba(16,24,40,0.08);padding:48px;display:block}

/* Responsive spacing */
@media (max-width:768px){.framed-section{padding:40px 0}.framed-section .framed-card{padding:24px;margin:0 16px;border-radius:22px}}
```

#### Standard Reader Card Implementation
```css
/* Content placeholder styling */
.framed-card__content{background:transparent}
.reader-placeholder{min-height:320px;border-radius:12px;border:3px solid rgba(59,130,246,0.12);padding:2rem;color:#0f172a;background:transparent}
```

#### Typography Standards
- **Brand Font**: 'Lora' (serif) - For logo and brand elements
- **UI Font**: 'Montserrat' (sans-serif) - For interface elements
- **Body Font**: 'Inter' (sans-serif) - Fallback for body text
- **Greek Text**: 'Montserrat' with font-weight:300, font-size:20px
- **Standard Blue**: #3b82f6 (Greek blue for borders and accents)

#### Hero Image Implementation
Each page requires a specific hero image in `/public/images/`:
- Landing page: `hero.jpg`
- Guided Reader: `guided-reader-pic.jpg`
- Psalms page: `psalms_hero_pic.jpg`
- [Add new pages with corresponding hero images]

#### Page-Specific Variations
- **Landing Page**: Full marketing layout with tools grid
- **Guided Reader**: Sidebar navigation + main reader area
- **Psalms Dashboard**: Top navigation bar + reader area
- **[Future pages]**: Follow same base structure with content variations

### Build Guidelines
1. **Always start with the standard HTML structure above**
2. **Include all required CSS base classes**
3. **Use exact typography specifications**
4. **Maintain consistent header and hero implementations**
5. **Replace `[PAGE_HERO_IMAGE]` with actual image filename**
6. **Keep logo routing and navigation consistent**
7. **Use identical border radius, padding, and shadow values**
8. **Ensure mobile responsiveness with provided media queries**

### 2. Content Processing Agent (Planned)
**Role**: Liturgical text processing and annotation
**Planned Capabilities**:
- Parse Greek text files
- Generate phonetic transcriptions
- Create grammar annotations
- Build lexicon entries
- Validate text accuracy

### 3. Learning Analytics Agent (Future)
**Role**: Track user progress and optimize learning paths
**Planned Capabilities**:
- Monitor user interactions
- Analyze learning patterns
- Suggest personalized exercises
- Generate progress reports

## Agent Interactions

## Technology Stack & Agent Integration

### Frontend Technologies
- **Vue.js 3**: Component-based architecture for interactive learning modules
- **Modern CSS**: Dark theme with Orthodox-inspired design elements
- **Drag & Drop API**: Text reconstruction exercises and word matching games
- **Responsive Design**: Mobile-first approach with thumb-zone optimized navigation
- **Typography System**: Professional 3-font combination for optimal readability and branding

### Typography & Design
- **Brand Font**: Lora (serif) - Calligraphic, warm feel for "Philolog" branding
- **Heading Font**: Inter (sans-serif) - Ultra-modern, clean for titles and navigation
- **Body Font**: Inter (sans-serif) - Highly readable for content and UI elements
- **Color Scheme**: Clean white background with blue accent colors
- **Hero Design**: Custom background image with subtle blue gradient overlay (30% opacity)

### Data Management
- **JSON Files**: Structured liturgical text storage in `/texts/` directory
- **Static Assets**: `/public/` folder for images and resources
- **File Organization**: Modular text files for individual prayers and liturgical excerpts
- **Unicode Support**: Proper Greek text encoding and display

### Development Workflow

### Development Workflow
1. **Code Generation**: GitHub Copilot assists with feature development
2. **Content Validation**: Automated checks for Greek text accuracy
3. **Testing**: Automated testing of interactive features
4. **Deployment**: Continuous integration for updates

### Data Flow
```
Raw Greek Texts → Content Processing → Structured JSON → Web Interface
                                    ↓
                              Learning Analytics ← User Interactions
```

## Development Milestones

### Phase 1: Complete ✅
- Basic HTML structure and Vue.js integration
- Text reader with hover tooltips and grammar color-coding
- Multiple liturgical texts loaded (15+ prayers and liturgical excerpts)
- Responsive design with mobile-optimized navigation
- Public assets folder structure created

### Phase 2: In Progress 🔄
- Text reconstruction game with drag-and-drop functionality
- Word matching exercises with difficulty levels
- Lexicon search and filtering system
- Root word tree visualization
- Fill-in-the-blank exercises

### Phase 3: Planned 📋
- Advanced parsing challenges with grammar identification
- Progress tracking and user analytics
- Voice recognition for pronunciation practice
- User authentication and personal learning paths
- Church calendar integration

## Orthodox Liturgical Context

### Text Sources
- Authentic liturgical texts from Orthodox tradition
- Proper ecclesiastical Greek usage and grammar
- Seasonal and festal variations included
- Texts range from basic prayers to complex liturgical excerpts

### Educational Goals
- Support Orthodox Christian education and catechesis
- Preserve liturgical language knowledge for future generations
- Bridge ancient liturgical texts with modern interactive learning
- Provide accessible entry point for Koine Greek study

### Content Standards
- Theologically accurate translations and glosses
- Consistent phonetic transcription system
- Grammar parsing aligned with liturgical context
- Respectful presentation of sacred texts

## Configuration Files

### Agent Settings
- `.github/copilot.yml` (if using GitHub Copilot for Teams)
- `package.json` for Node.js dependencies
- Custom configuration files as needed

### API Keys and Secrets
- Store sensitive information in environment variables
- Use `.env` files for local development
- Secure API endpoints for production

## Best Practices

### Code Quality
- Use consistent naming conventions
- Maintain proper file structure
- Document all major functions
- Regular code reviews with AI assistance

### Content Management
- Validate all Greek text against liturgical sources
- Maintain consistent JSON structure
- Regular backups of text files
- Version control for content updates

### Security
- Sanitize all user inputs
- Secure API endpoints
- Regular security audits
- Privacy-compliant data handling

## Future Enhancements

### Planned Agent Features
1. **Multi-language Support**: Expand beyond Greek to other liturgical languages
2. **Advanced Grammar Engine**: More sophisticated parsing and analysis
3. **Adaptive Learning**: AI-powered personalization
4. **Voice Recognition**: Pronunciation practice assistance

### Integration Opportunities
- Church calendar integration
- Digital liturgical books
- Online liturgical services
- Educational institution partnerships

## Monitoring and Maintenance

### Performance Metrics
- Page load times
- User engagement rates
- Learning completion rates
- Error frequencies

### Regular Tasks
- Update Greek text databases
- Refresh lexicon entries
- Monitor user feedback
- System health checks

---

**Last Updated**: January 12, 2026
**Maintained By**: Project Development Team
**Contact**: [Add contact information as needed]